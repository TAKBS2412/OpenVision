#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include "Networking.cpp"
#include "ImageFiltering.cpp"
#include "ImageProc.cpp"
#include "TargetProc.cpp"
#include <time.h>

int round2(double);

int main() {
	ImageFiltering imageFilter = ImageFiltering();
	ImageProc imageProc = ImageProc();
	TargetProc targetProc = TargetProc();
	clock_t t;
	char hostname[] = "192.168.0.10"; //TODO Change this to 10.24.12.2
	int port = 2412;
	Networking networking = Networking(hostname, port);
	while(1) {
		cv::Mat img;
		cv::Mat newimg(480, 640, CV_8UC3, cv::Scalar(0, 0, 0));

		img = cv::imread("/home/ubuntu/src/jetson/faketargets.png", cv::IMREAD_COLOR);
		t = clock() - t;
		std::cout << "ImageFiltering - Time elapsed (s): " << ((float)t)/CLOCKS_PER_SEC << "\n";
		
		cv::vector<cv::vector<cv::Point> > contours;
		cv::vector<cv::vector<cv::Point> > goodcontours;
		cv::vector<cv::Vec4i> hierarchy;
		int error = 0;
		t = clock();
		goodcontours = imageProc.procImage(img, contours, goodcontours, hierarchy, error);
		t = clock() - t;
		std::cout << "ImageProc - Time elapsed (s): " << ((float)t)/CLOCKS_PER_SEC << "\n";

		if(error == 1) {
			return 1;
		}
		t = clock();
		targetProc.procTarget(newimg, goodcontours, networking);
		t = clock() - t;
		std::cout << "TargetProc - Time elapsed (s): " << ((float)t)/CLOCKS_PER_SEC << "\n";

		cv::imshow("Hello!", newimg);
		char c = cv::waitKey(1);
		if(c == 'q') {
			break;
		}
	}
	networking.closeSocket();
}
