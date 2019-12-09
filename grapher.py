import _thread
from time import sleep
import matplotlib.pyplot as plt
import numpy as np

class InternetGraph:

	def __init__(self):
		self._dataset = []
		_thread.start_new_thread(self.run, ())

	def _plot(self):
		ds_len = len(self._dataset)

		plt.ion()
		plt.clf()

		plt.plot(np.linspace(0,ds_len,ds_len), np.array(list(map(lambda x: x[0], self._dataset))), "ro", label='Download', linestyle='--')
		plt.plot(np.linspace(0,ds_len,ds_len), np.array(list(map(lambda x: x[1], self._dataset))), "go", label='Upload', linestyle='-')
		plt.ylim(ymin=0)
		plt.xlabel("Test Number (#)")
		plt.ylabel("Download & Upload Speeds (Mbps)")

		plt.draw()
		plt.pause(0.01)

	def update(self, row):
		self._dataset.append(row)

	def run(self):
		while True:
			self._plot()
			sleep(1)