#include <opencv2/imgproc/imgproc.hpp>

class ImageFiltering {
	public:
	void filterImage(cv::Mat &img, cv::Mat &newimg) {
		clock_t t;
		int lowerh = 50;
		int lowers = 200;
		int lowerv = 30;
		int higherh = 66;
		int highers = 255;
		int higherv = 255;
	
		cv::cvtColor(img, newimg, CV_BGR2HSV);
		
		t = clock();
		cv::inRange(newimg, cv::Scalar(lowerh, lowers, lowerv), cv::Scalar(higherh, highers, higherv), newimg);
		t = clock() - t;
		std::cout << "ImageFiltering (inRange) - Time elapsed (s): " << ((float)t)/CLOCKS_PER_SEC << "\n";
	}
};
