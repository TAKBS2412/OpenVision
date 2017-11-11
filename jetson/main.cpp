#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>

int main() {
	cv::Mat img;
	cv::Mat newimg(480, 640, CV_8UC3, cv::Scalar(0, 0, 0));

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
	cv::vector<cv::Point> largestContour;
	cv::vector<cv::Point> secondLargestContour;

	if(contours.size() < 2) {
		std::cout << "Not enough contours!\n";
	} else {
		double largestContourArea = 0; // Area of the largest contour
		double secondLargestContourArea = 0; // Area of the largest contour
				
		int i;
		for(i = 0; i < contours.size(); i++) {
			cv::vector<cv::Point> currentContour = contours[i];
			double contourArea = cv::contourArea(currentContour);
			cv::vector<cv::Point> approx;
			cv::approxPolyDP(currentContour, approx, 0.05*cv::arcLength(currentContour, true), true);

			if(approx.size() != 4) {
				continue;
			}

			double polygonArea = cv::contourArea(approx);
			if(polygonArea == 0 || contourArea == 0) {
				continue;
			}
			double percentFilled = polygonArea/contourArea*100;
			if(percentFilled < 70) {
				continue;
			}

			if(contourArea > largestContourArea) {
				secondLargestContourArea = largestContourArea;
				secondLargestContour = largestContour;
				largestContourArea = contourArea;
				largestContour = currentContour;
			} else if(contourArea > secondLargestContourArea) {
				secondLargestContourArea = contourArea;
				secondLargestContour = currentContour;
			}
		}
		cv::vector<cv::vector<cv::Point> > goodcontours = cv::vector<cv::vector<cv::Point> >();
		goodcontours.push_back(secondLargestContour);
		goodcontours.push_back(largestContour);
		std::cout << "Number of contours: " << goodcontours.size() << "\n";	
		cv::Scalar color(0, 225, 0);
		cv::drawContours(newimg, goodcontours, -1, color, CV_FILLED);
		cv::Rect rect;
		rect = cv::boundingRect(largestContour);
		double hpx = rect.size().height;		
		std::cout << "Height: " << hpx << "\n";
		double distance = (480*5.08)/(2*hpx*tan(0.726/2));
		std::cout << "Distance: " << distance << "\n";
	

	}

	//cv::imshow("Hello!", newimg);
	//cv::waitKey();
}
