#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include "ImageFiltering.cpp"

int round2(double);

int main() {
	ImageFiltering imageFilter = ImageFiltering();
	while(1) {
		cv::Mat img;
		cv::Mat newimg(480, 640, CV_8UC3, cv::Scalar(0, 0, 0));

		img = cv::imread("/home/ubuntu/src/jetson/faketargets.png", cv::IMREAD_COLOR);
		/*
		cv::cvtColor(img, img, CV_BGR2HSV);
		int lowerh = 50;
		int lowers = 200;
		int lowerv = 30;
		int higherh = 66;
		int highers = 255;
		int higherv = 255;

		cv::inRange(img, cv::Scalar(lowerh, lowers, lowerv), cv::Scalar(higherh, highers, higherv), img);
		*/
		img = imageFilter.filterImage(img);
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
			cv::Moments moments = cv::moments(largestContour);
			if(moments.m00 == 0) {
				std::cout << "Invalid moments!\n";
				return 1;
			} 
			int cx = round2(moments.m10/moments.m00);
			int cy = round2(moments.m01/moments.m00);
			std::cout << "(" << cx << ", " << cy << ")\n";
			cv::Moments moments2 = cv::moments(secondLargestContour);
			if(moments2.m00 == 0) {
				std::cout << "Invalid moments!\n";
				return 1;
			} 
			int cx2 = round2(moments2.m10/moments2.m00);
			int cy2 = round2(moments2.m01/moments2.m00);
			std::cout << "(" << cx2 << ", " << cy2 << ")\n";
			double pegx = (cx+cx2)/2;
			double angle = atan(5.08*(pegx-320)/(hpx*distance));
			std::cout << "Angle: " << angle << "\n";

		}

		cv::imshow("Hello!", newimg);
		char c = cv::waitKey(1);
		if(c == 'q') {
			break;
		}
	}
}

int round2(double a) {
	if(a < 0) {
		a -= 0.5;
	} else if(a > 0) {
		a += 0.5;
	}
	return (int) a;
}
