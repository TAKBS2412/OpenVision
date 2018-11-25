#include <opencv2/imgproc/imgproc.hpp>

class ImageProc {
	public:
	std::vector<std::vector<cv::Point> >& procImage(cv::Mat &img, std::vector<std::vector<cv::Point> > &oldContours, std::vector<std::vector<cv::Point> > &newContours, std::vector<cv::Vec4i> &hierarchy, int *error) {

		cv::findContours(img.clone(), oldContours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_TC89_KCOS);
		std::vector<cv::Point> largestContour;
		std::vector<cv::Point> secondLargestContour;

		if(oldContours.size() < 2) {
			std::cerr << "Not enough contours!\n";
			*error = 1;
		} else {
			double largestContourArea = 0; // Area of the largest contour
			double secondLargestContourArea = 0; // Area of the largest contour
					
			int i;
			for(i = 0; i < oldContours.size(); i++) {
				std::vector<cv::Point> currentContour = oldContours[i];
				double contourArea = cv::contourArea(currentContour);
				std::vector<cv::Point> approx;
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
		}
		newContours.push_back(largestContour);
		newContours.push_back(secondLargestContour);
		error = 0;
		return newContours;
	}
};
