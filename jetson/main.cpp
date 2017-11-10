#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>

int main() {
	cv::Mat img;

	img = cv::imread("/home/ubuntu/src/jetson/faketargets.png", cv::IMREAD_COLOR);
	cv::cvtColor(img, img, CV_BGR2HSV);
	int lowerh = 50;
	int lowers = 200;
	int lowerv = 30;
	int higherh = 66;
	int highers = 255;
	int higherv = 255;

	cv::inRange(img, cv::Scalar(lowerh, lowers, lowerv), cv::Scalar(higherh, highers, higherv), img);
	
	cv::vector<cv::vector<cv::Point> > contours;
	cv::vector<cv::Vec4i> hierarchy;

	cv::findContours(img.clone(), contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_TC89_KCOS);

	std::cout << contours.size();

	cv::imshow("Hello!", img);
	cv::waitKey();
}
