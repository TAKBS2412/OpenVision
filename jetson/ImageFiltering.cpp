#include <opencv2/imgproc/imgproc.hpp>

class ImageFiltering {
	public:
	cv::Mat& filterImage(cv::Mat &img) {
	 	cv::cvtColor(img, img, CV_BGR2HSV);
		int lowerh = 50;
		int lowers = 200;
		int lowerv = 30;
		int higherh = 66;
		int highers = 255;
		int higherv = 255;

		cv::inRange(img, cv::Scalar(lowerh, lowers, lowerv), cv::Scalar(higherh, highers, higherv), img);
		
		return img;
	}
};
