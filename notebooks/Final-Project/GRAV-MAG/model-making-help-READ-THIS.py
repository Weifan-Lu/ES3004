# !!! DO NOT ACTUALLY TRY TO EXECUTE THE CODE EXACTLY AS IT IS WRITTEN IN THIS FILE !!!
# !!! IT WILL NOT RUN IF YOU JUST COPY-PASTE WITHOUT FIRST FIGURING OUT WHAT ELSE YOU NEED !!!
# !!! THIS IS MEANT TO HELP YOU FIGURE OUT HOW TO MAKE YOUR GRAVITY AND MAGNETIC MODEL !!!

# first set up the region and shape to match the seismic survey set up:
region      = (0, 50000, 0, 50000)  # (x_min, x_max, y_min, y_max), all in meters
shape       = (51, 51)              # (n_x, n_y)
height      = 0                     # height where the measurement should be made, in meters
coordinates = vd.grid_coordinates(region, shape=shape, extra_coords=height)

# then load the data file:
data = pd.read_csv("path/to/default_gravity.csv")

# do some other steps here (like make your model, etc.)

# key point when making the block for either gravity or magnetic:
block = [[x_min, x_max, 0, 50000, z_min, z_max]] # <- BE CAREFUL: make it 2D like in the labs by using the entire y domain
# continue making your model... 

# for magnetics: only change the 'magnetization' in y, e.g.:
magnetization = np.array([0, VARIABLE, 0]) # <- ONLY change the VARIABLE part, don't change the zeros

# then, to get the data and your model to plot on the same axes (for curve fitting):
plt.figure(figsize=(14,5), dpi=200)
plt.plot(data['X distance [m]'],model_result[25], label='Model fit to data')
plt.scatter(data['X distance [m]'], data['Gravity Anomaly [mGal]'], label='Default data')
plt.ylabel('Gravity Anomaly [mGal]')
plt.xlabel('Distance, (orientation on map) [m]')
plt.xlim(0,50000)
plt.grid()
plt.legend()
plt.show();

# the above for plotting also works for magnetic data, but you will need to index the model output differently:
# model_result[50] for magnetic data (model_result should be b_z in the magnetics case) instead of model_result[25] for gravity
