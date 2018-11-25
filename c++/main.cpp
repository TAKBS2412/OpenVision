#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include "Networking.cpp"
#include "ImageFiltering.cpp"
#include <time.h>

int round2(double);

int main() {
	ImageFiltering imageFilter = ImageFiltering();
	//ImageProc imageProc = ImageProc();
	//TargetProc targetProc = TargetProc();
	clock_t t;
	char hostname[] = "192.168.0.10"; //TODO Change this to 10.24.12.2
	int port = 2412;
	//Networking networking = Networking(hostname, port);
	const std::string cameraAddress = "http://192.168.0.11/mjpg/video.mjpg";
	cv::VideoCapture vcap(cameraAddress);
	while(1) {
		cv::Mat img;
		cv::Mat newimg(480, 640, CV_8UC3, cv::Scalar(0, 0, 0));

		t = clock();
		//img = cv::imread("/home/ubuntu/src/jetson/faketargets.png", cv::IMREAD_COLOR);
		//vcap >> img;	
		img = cv::imread("../waamv/orig1.jpg");
		imageFilter.filterImage(img, newimg);
		t = clock() - t;
		std::cout << "ImageFiltering - Time elapsed (s): " << ((float)t)/CLOCKS_PER_SEC << "\n";
		/*
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
		*/
		/*goodcontours = imageProc.procImage(img, contours, goodcontours, hierarchy, &error);
		if(error == 0) {
			targetProc.procTarget(newimg, goodcontours);
		}*/
		cv::imshow("Original Frame: ", img);
		cv::imshow("Processed Frame: ", newimg);
		char c = cv::waitKey(1);
		if(c == 'q') {
			break;
		}
	}
	//networking.closeSocket();
}
