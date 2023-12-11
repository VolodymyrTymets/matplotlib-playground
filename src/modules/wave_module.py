import numpy as np
import struct
import matplotlib.animation as animation
import matplotlib.ticker as ticker

from src.modules.config_module import nFFT, RATE, FPS, MAX_AMPLITUDE

class Wave:
  def __init__(self, theme):
      self.y_L = [];  
      self.y_R = [];
      self.label = None;
      self.theme = theme;
  
  def on_data(self, y_L, y_R, y):
    self.y_L = y_L;
    self.y_R = y_R
       
  def animate(self, i, line, stream, wf, MAX_y):
    Y = np.hstack((self.y_L[::2], self.y_R[::2]));
    y_data = line.get_ydata();
    new_y_data = y_data[len(Y):len(y_data)];
    line.set_ydata(np.concatenate((new_y_data, Y)))
    mean = np.mean(np.abs(Y))
    if(self.label.set_text):
      percent = 0 if mean == 0 else int(mean / (MAX_AMPLITUDE) * 100)
      self.label.set_text(u"A:{}/{}%".format(int(mean), percent))
    
    return line, self.label

  def clear(self, line):
    return line,

  def init(self, fig, ax): 
    # Frequency range
    x_f = 1.0 * np.arange(1, RATE) / nFFT * RATE
    ax.set_yscale('linear');
    ax.set_xlim(x_f[0], x_f[-1]);
    ax.set_ylim(-1 *  MAX_AMPLITUDE, MAX_AMPLITUDE); 
    ax.xaxis.set_major_locator(ticker.NullLocator()) 
    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.set_facecolor(self.theme.get_face_color())
    ax.spines['top'].set_color(self.theme.get_border_color())
    ax.spines['bottom'].set_color(self.theme.get_border_color())
    ax.spines['left'].set_color(self.theme.get_border_color())
    ax.spines['right'].set_color(self.theme.get_border_color())
    
    line, = ax.plot(x_f, np.zeros(RATE - 1), linewidth=1, color=self.theme.get_line_color())
    self.label = ax.text(0.1,0.9, "", bbox={'facecolor':'w', 'alpha':0, 'pad':5},
                transform=ax.transAxes, ha="center", color=self.theme.get_text_color())

    frames = None
    wf = None
    stream = None
    MAX_y = None
    ani = animation.FuncAnimation(
      fig, self.animate, frames,
      init_func=lambda: self.clear(line), fargs=(line, stream, wf, MAX_y),
      cache_frame_data=False,
      interval=1000.0 / FPS, blit=True
    )
    return ani;