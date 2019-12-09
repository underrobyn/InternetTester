import speedtest
import time
from grapher import InternetGraph

file_headers = 'sever_time, client_time, download, upload, ping, downloaded, uploaded, serverid, clientisp, clientip, shareurl,\n'
file_name = "speeds_%s.csv" % time.time()
test_interval = 5
servers = []
threads = None
graph = InternetGraph()


def bps_to_mbps(n):
	return round(float(n)/1048576,2)

def b_to_mb(n):
	return round(float(n)/8388608,2)

def get_metrics(result):
	return {
		"servertime":result["timestamp"],
		"clienttime":time.time(),
		"download":round(result["download"],4),
		"upload":round(result["upload"],4),
		"ping":result["ping"],
		"downloaded":round(result["bytes_received"],4),
		"uploaded":round(result["bytes_sent"],4),
		"serverid":result["server"]["id"],
		"clientisp":result["client"]["isp"],
		"clientip":result["client"]["ip"],
		"shareimg":result["share"]
	}


def run_test():
	s = speedtest.Speedtest()
	logger("[Speedtest Object] -> Created")

	s.get_servers(servers)
	s.get_best_server()
	logger("[Speedtest Object] -> Found best server")

	s.download(threads=threads)
	logger("[Speedtest Object] -> Completed download test")

	s.upload(threads=threads)
	logger("[Speedtest Object] -> Completed upload test")

	s.results.share()
	logger("[Speedtest Object] -> Data logged to speedtest.net")
	print (s.results.dict())

	return get_metrics(s.results.dict())


def exec_speedtest():
	start_time = time.time()
	logger("\nSpeed test started at: %s" % start_time)

	test_data = run_test()
	logger("[Speedtest Object] -> Results compiled.")

	end_time = time.time()

	test_data["test_duration"] = end_time - start_time

	log_csv(test_data)

	return test_data


def pretty_print(data):
	global graph_data

	test_dur = round(float(data["test_duration"]),2)

	download_speed_mbps = bps_to_mbps(data["download"])
	download_speed_mb = b_to_mb(data["download"])

	upload_speed_mbps = bps_to_mbps(data["upload"])
	upload_speed_mb = b_to_mb(data["upload"])

	download_data_mb = bps_to_mbps(data["downloaded"])
	upload_data_mb = bps_to_mbps(data["uploaded"])

	graph.update([download_speed_mbps, upload_speed_mbps])

	print("\nTest Completed (Took %ss)!\nDownload Speed: %sMb/s [%sMB/s] (Data Used: %sMB)\nUpload Speed: %sMb/s [%sMB/s] (Data Used: %sMB)" %
	      (test_dur, download_speed_mbps, download_speed_mb, download_data_mb, upload_speed_mbps, upload_speed_mb, upload_data_mb))


def logger(line):
	if False: print(line)


def output_file(line):
	with open(file_name, "a") as f:
		f.write(line)


def log_csv(dict):
	row = ""
	for i in dict:
		row = "%s%s," % (row, dict[i])

	row = row + '\n'
	output_file(row)


def main():
	# Write CSV headers
	output_file(file_headers)

	while True:
		data = exec_speedtest()
		pretty_print(data)
		time.sleep(test_interval)


if __name__ == "__main__":
	main()