#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

int main() {
	//cv::Mat img(512, 512, CV_8UC3, cv::Scalar(0));
	cv::Mat img;

	img = cv::imread("/home/ubuntu/src/jetson/test.png", cv::IMREAD_COLOR);
	//cv::putText(img, "Hello, world!", cv::Point(10, img.rows/2), cv::FONT_HERSHEY_DUPLEX, 1.0, CV_RGB(118, 185, 0), 2);
	cv::cvtColor(img, img, CV_BGR2HSV);

	cv::imshow("Hello!", img);
	cv::waitKey();
}
