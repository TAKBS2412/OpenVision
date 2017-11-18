#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include "ImageFiltering.cpp"
#include "ImageProc.cpp"
#include "TargetProc.cpp"

int round2(double);

int main() {
	ImageFiltering imageFilter = ImageFiltering();
	ImageProc imageProc = ImageProc();
	TargetProc targetProc = TargetProc();
	while(1) {
		cv::Mat img;
		cv::Mat newimg(480, 640, CV_8UC3, cv::Scalar(0, 0, 0));

		img = cv::imread("/home/ubuntu/src/jetson/faketargets.png", cv::IMREAD_COLOR);
		
		img = imageFilter.filterImage(img);
		cv::vector<cv::vector<cv::Point> > contours;
		cv::vector<cv::vector<cv::Point> > goodcontours;
		cv::vector<cv::Vec4i> hierarchy;
		int error = 0;
		goodcontours = imageProc.procImage(img, contours, goodcontours, hierarchy, error);
		if(error == 1) {
			return 1;
		}
		targetProc.procTarget(newimg, goodcontours);
		cv::imshow("Hello!", newimg);
		char c = cv::waitKey(1);
		if(c == 'q') {
			break;
		}
	}
}
