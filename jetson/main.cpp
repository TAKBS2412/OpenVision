#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include "ImageFiltering.cpp"
#include "ImageProc.cpp"

int round2(double);

int main() {
	ImageFiltering imageFilter = ImageFiltering();
	ImageProc imageProc = ImageProc();
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
		cv::vector<cv::Point> largestContour = goodcontours[0];
		cv::vector<cv::Point> secondLargestContour = goodcontours[1];

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
