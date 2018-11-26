#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

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

		cv::GaussianBlur(img, img, cv::Size(5, 5), 0, 0);
	
		cv::cvtColor(img, img, CV_BGR2HSV);
	
		cv::Mat HSVmask;
	
		t = clock();
		cv::inRange(img, cv::Scalar(lowerh, lowers, lowerv), cv::Scalar(higherh, highers, higherv), HSVmask);
		t = clock() - t;
		std::cout << "ImageFiltering (inRange) - Time elapsed (s): " << ((float)t)/CLOCKS_PER_SEC << "\n";
		
		cv::bitwise_and(img, img, newimg, HSVmask);
		cv::imshow("Test", newimg);

		cv::cvtColor(newimg, newimg, CV_BGR2GRAY);	
	}
};
