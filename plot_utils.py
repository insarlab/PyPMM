import os
import numpy as np

from shapely import geometry

import matplotlib.pyplot as plt
from cartopy import crs as ccrs, feature as cfeature

####################################  Utility for plotting  ##############################################
# Utility for plotting the plate motion on a globe
# check usage: https://github.com/yuankailiu/utils/blob/main/notebooks/PMM_plot.ipynb
# Later will be moved to a separate script `plot_utils.py` in plate motion package

def read_plate_outline(pmm_name='GSRM', plate_name=None):
    """Read the plate boundaries for the given plate motion model.

    Paramters: pmm_name   - str, plate motion (model) name
               plate_name - str, plate name of interest, return all plates if None
    Returns:   outline    - dict, a dictionary that contains lists of vertices in lat/lon for all plates
                            OR shapely.geometry.polygon.Polygon object, boundary of the given "plate".
    """

    # check input
    if 'GSRM' in pmm_name:
        pmm_name = 'GSRM'
        pmm_dict = GSRM_V21_PMM

    elif 'MORVEL' in pmm_name:
        pmm_name = 'MORVEL'
        pmm_dict = NNR_MORVEL56_PMM

    else:
        msg = f'Un-recognized plate motion model: {pmm_name}!'
        msg += '\nAvailable models: GSRM, MORVEL.'
        raise ValueError(msg)

    # plate boundary file
    plate_boundary_file = PLATE_BOUNDARY_FILE[pmm_name]
    coord_order = os.path.basename(plate_boundary_file).split('.')[-1]
    if coord_order not in ['lalo', 'lola']:
        raise ValueError(f'Can NOT recognize the lat/lon order from the file extension: .{coord_order}!')

    # dict to convert plate abbreviation to name
    plate_abbrev2name = {}
    for key, val in pmm_dict.items():
        plate_abbrev2name[val.Abbrev.upper()] = key

    # read the plate outlines file, save them to a dictionary {plate_A: [vertices], ..., ..., ...}
    outlines = {}
    with open(plate_boundary_file) as f:
        lines = f.readlines()
        key, vertices = None, None
        # loop over lines to read
        for line in lines:
            # whether we meet a new plate name abbreviation
            if line.startswith('> ') or line.startswith('# ') or len(line.split()) == 1:
                # whether to add the previous plate to the dictionary
                if key and vertices:
                    pname = plate_abbrev2name[key]
                    outlines[pname] = np.array(vertices)
                # identify the new plate name abbreviation
                if line.startswith('> '):
                    key = line.split('> ')[1]
                elif line.startswith('# '):
                    key = line.split('# ')[1]
                else:
                    key = str(line)
                # remove the line change string
                if key.endswith('\n'):
                    key = key.split('\n')[0]
                # new vertices for the new plate
                vertices = []

            # get plate outline vertices
            else:
                vert = np.array(line.split()).astype(float)
                if coord_order == 'lola':
                    vert = np.flip(vert)
                vertices.append(vert)

    # outline of a specific plate
    if plate_name:
        if plate_name not in plate_abbrev2name.values():
            plate_abbrev = pmm_dict[plate_name].Abbrev
            raise ValueError(f'Can NOT found plate {plate_name} ({plate_abbrev}) in file: {plate_boundary_file}!')

        # convert list into shapely polygon object
        # for easy use
        outline = geometry.Polygon(outlines[plate_name])

    else:
        outline = outlines

    return outline


def plot_plate_motion(plate_boundary, epole_obj, center_lalo=None, qscale=200, qunit=50,
                      satellite_height=1e6, figsize=[5, 5], **kwargs):
    """Plot the globe map wityh plate boundary, quivers on some points.

    Parameters: plate_boundary   - shapely.geometry.Polygon object
                epole_obj        - mintpy.objects.euler_pole.EulerPole object
                center_lalo      - list of 2 float, center the map at this latitute, longitude
                qscale           - float, scaling factor of the quiver
                qunit            - float, length of the quiver legend in mm/yr
                satellite_height - height of the perspective view looking in meters
                kwargs           - dict, dictionary for plotting
    Returns:    fig, ax          - matplotlib figure and axes objects
    Examples:
        from matplotlib import pyplot as plt
        from mintpy.objects import euler_pole
        from shapely import geometry

        # build EulerPole object
        plate_pmm = euler_pole.ITRF2014_PMM['Arabia']
        epole_obj = euler_pole.EulerPole(wx=plate_pmm.omega_x, wy=plate_pmm.omega_y, wz=plate_pmm.omega_z)

        # read plate boundary
        plate_boundary = euler_pole.read_plate_outline('GSRM', 'Arabia')

        # plot plate motion
        fig, ax = euler_pole.plot_plate_motion(plate_boundary, epole_obj)
        plt.show()
    """

    def _sample_coords_within_polygon(polygon_obj, ny=10, nx=10):
        """Make a set of points inside the defined sphericalpolygon object.

        Parameters: polygon_obj - shapely.geometry.Polygon, a polygon object in lat/lon.
                    ny          - int, number of intial sample points in the y (lat) direction.
                    nx          - int, number of intial sample points in the x (lon) direction.
        Returns:    sample_lats - 1D np.ndarray, sample coordinates   in the y (lat) direction.
                    sample_lons - 1D np.ndarray, sample coordinates   in the x (lon) direction.
        """
        # generate sample point grid
        poly_lats = np.array(polygon_obj.exterior.coords)[:,0]
        poly_lons = np.array(polygon_obj.exterior.coords)[:,1]
        cand_lats, cand_lons = np.meshgrid(
            np.linspace(np.min(poly_lats), np.max(poly_lats), ny),
            np.linspace(np.min(poly_lons), np.max(poly_lons), nx),
        )
        cand_lats = cand_lats.flatten()
        cand_lons = cand_lons.flatten()

        # select points inside the polygon
        flag = np.zeros(cand_lats.size, dtype=np.bool_)
        for i, (cand_lat, cand_lon) in enumerate(zip(cand_lats, cand_lons)):
            if polygon_obj.contains(geometry.Point(cand_lat, cand_lon)):
                flag[i] = True
        sample_lats = cand_lats[flag]
        sample_lons = cand_lons[flag]

        return sample_lats, sample_lons

    # default plot settings
    kwargs['c_ocean']     = kwargs.get('c_ocean', 'w')
    kwargs['c_land']      = kwargs.get('c_land', 'lightgray')
    kwargs['c_plate']     = kwargs.get('c_plate', 'mistyrose')
    kwargs['lw_coast']    = kwargs.get('lw_coast', 0.5)
    kwargs['lw_pbond']    = kwargs.get('lw_pbond', 1)
    kwargs['lc_pbond']    = kwargs.get('lc_pbond', 'coral')
    kwargs['alpha_plate'] = kwargs.get('alpha_plate', 0.4)
    kwargs['grid_ls']     = kwargs.get('grid_ls', '--')
    kwargs['grid_lw']     = kwargs.get('grid_lw', 0.3)
    kwargs['grid_lc']     = kwargs.get('grid_lc', 'gray')
    kwargs['qnum']        = kwargs.get('qnum', 6)
    # point of interest
    kwargs['pts_lalo']    = kwargs.get('pts_lalo', None)
    kwargs['pts_marker']  = kwargs.get('pts_marker', '^')
    kwargs['pts_ms']      = kwargs.get('pts_ms', 20)
    kwargs['pts_mfc']     = kwargs.get('pts_mfc', 'r')
    kwargs['pts_mec']     = kwargs.get('pts_mec', 'k')
    kwargs['pts_mew']     = kwargs.get('pts_mew', 1)

    # map projection
    # based on: 1) map center and 2) satellite_height
    if not center_lalo:
        if kwargs['pts_lalo']:
            center_lalo = kwargs['pts_lalo']
        else:
            center_lalo = np.array(plate_boundary.centroid.coords)[0]
    map_proj = ccrs.NearsidePerspective(center_lalo[1], center_lalo[0], satellite_height=satellite_height)

    # make a base map from cartopy
    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(projection=map_proj))
    ax.set_global()
    ax.gridlines(color=kwargs['grid_lc'],
                 linestyle=kwargs['grid_ls'],
                 linewidth=kwargs['grid_lw'],
                 xlocs=np.arange(-180,180,30),
                 ylocs=np.linspace(-80,80,10))
    ax.add_feature(cfeature.OCEAN, color=kwargs['c_ocean'])
    ax.add_feature(cfeature.LAND,  color=kwargs['c_land'])
    ax.add_feature(cfeature.COASTLINE, linewidth=kwargs['lw_coast'])

    # add the plate polygon
    if plate_boundary:
        poly_lats = np.array(plate_boundary.exterior.coords)[:, 0]
        poly_lons = np.array(plate_boundary.exterior.coords)[:, 1]
        ax.plot(poly_lons, poly_lats, color=kwargs['lc_pbond'], transform=ccrs.Geodetic(), linewidth=kwargs['lw_pbond'])
        ax.fill(poly_lons, poly_lats, color=kwargs['c_plate'],  transform=ccrs.Geodetic(), alpha=kwargs['alpha_plate'])

        # compute the plate motion from Euler rotation
        if epole_obj:
            # select sample points inside the polygon
            sample_lats, sample_lons = _sample_coords_within_polygon(plate_boundary, ny=kwargs['qnum'], nx=kwargs['qnum'])

            # calculate plate motion on sample points
            ve, vn = epole_obj.get_velocity_enu(lat=sample_lats, lon=sample_lons)[:2]

            # scale from m/yr to mm/yr
            ve *= 1e3
            vn *= 1e3
            norm = np.sqrt(ve**2 + vn**2)

            # correcting for "East" further toward polar region; re-normalize ve, vn
            ve /= np.cos(np.deg2rad(sample_lats))
            renorm = np.sqrt(ve**2 + vn**2)/norm
            ve /= renorm
            vn /= renorm

            # ---------- plot inplate vectors --------------
            q = ax.quiver(sample_lons, sample_lats, ve, vn,
                          transform=ccrs.PlateCarree(), scale=qscale,
                          width=.0075, color='coral', angles="xy")
            # legend
            # put an empty title for extra whitepace at the top
            ax.set_title('  ', pad=10)
            ax.quiverkey(q, X=0.3, Y=0.9, U=qunit, label=f'{qunit} mm/yr', labelpos='E', coordinates='figure')

    # add custom points (e.g., show some points of interest)
    if kwargs['pts_lalo']:
        ax.scatter(kwargs['pts_lalo'][1], kwargs['pts_lalo'][0],
                   marker=kwargs['pts_marker'], s=kwargs['pts_ms'],
                   fc=kwargs['pts_mfc'], ec=kwargs['pts_mec'],
                   lw=kwargs['pts_mew'], transform=ccrs.PlateCarree())

    return fig, ax
