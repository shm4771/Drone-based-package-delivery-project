import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import k_mean as km
import random as rnd

# First set up the figure, the axis, and the plot element we want to animate


def main(speed, means, clusters, Solution):

  ## find radius from two array
  def Radius(cluster, mean):
    distances = []
    for point in cluster:
      distances.append(km.EuclideanDistance(point, mean))
    #print(distances)

    radius = max(val for (idx, val) in enumerate(distances))
    #print(radius)
    if(radius == None):
      return 1
    else:
      return radius


  ##plot clusters
  def PlotClusters(figure,ax, means, clusters):
    n = len(clusters)
    colors = ['r', 'b', 'g', 'y', 'c', 'm', 'k']

    for i in range(n):
      cluster = clusters[i]
      mean = means[i]
      c = rnd.choice(colors)
      colors.remove(c)

      Xa = []
      Xb = []
      for item in cluster:
        Xa.append(item[0])
        Xb.append(item[1])

      radius = Radius(cluster, mean)
      disk1 = plt.Circle((mean[0], mean[1]), radius, color=c, fill=False)
      ax.add_artist(disk1)
      plt.plot(Xa, Xb, 'o', color=c)
      plt.Circle((0,0), 5, color='g')

    return 0

    plt.show(block=False)

  # initialization function: plot the background of each frame
  def init():
      line.set_data([], [])
      return line,

  # animation function.  This is called sequentially
  def animate(i):
      x = X[i][0]
      y = X[i][1]
      #if((x == 0) & (X_store[len(X_store)-1]==0)&(y==0)&(Y_store[len(Y_store)-1]==0)):
        #print(X)
        #return line,
      #else:
      X_store.append(x)
      Y_store.append(y)
      line.set_data(X_store, Y_store)
      return line,

  
  ##Variables and animation calls
  print("Welcome to animation part")
  Feasible_k_value = len(means)

  X = []
  for i in range(Feasible_k_value):
    for j in range(len(Solution[i])):
      for k in range(len(Solution[i][j])):
        X.append([Solution[i][j][k][0], Solution[i][j][k][1]])

  X_store = []
  Y_store = []
  X_store.append(0)
  Y_store.append(0)


  fig = plt.figure()
  
  print()

  ax = plt.axes(xlim=(2*min(min(X)), 2*max(max(X))), ylim=(2*min(min(X)), 2*max(max(X))))
  line, = ax.plot([], [], 'r--', lw = 2)



  PlotClusters(fig, ax, means, clusters)
  anim = animation.FuncAnimation(fig, animate, init_func=init,
                                 frames=len(X)-1, interval=speed, blit=True)
  anim.save('path_animation2.mp4', fps=25, extra_args=['-vcodec', 'libx264'])
  plt.show()

  