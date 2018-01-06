#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/gpu/gpu.hpp>
int main() {
	//cv::gpu::GpuMat gmat;
	//cv::gpu::split(gmat, NULL);
	//const std::string address = "http://192.168.0.11/mjpg/video.mjpg";
	//cv::VideoCapture vcap(address);
	//cv::VideoCapture vcap("v4l2src ! ffmpegcolorspace ! appsink");
	//cv::VideoCapture vcap("v4l2src ! ffmpegcolorspace ! video/x-raw-rgb ! appsink");
	cv::VideoCapture vcap(0);
	//vcap.set(CV_CAP_PROP_FRAME_WIDTH, 640);
	//vcap.set(CV_CAP_PROP_FRAME_HEIGHT, 480);
	//cv::VideoCapture vcap(0);
	cv::Mat mat;
	//cout << cv::getBuildInformation() << endl;
	char c;
	do {
		//std::cout << "Hello, world!\n";
		vcap >> mat;
		//cv::imwrite("opened.jpg", mat);
		cv::imshow("Hello!", mat);
	} while((c = cv::waitKey(1)) != 'q');
	//std::cout << "OpenCV Version: " << CV_MAJOR_VERSION << "." << CV_MINOR_VERSION << std::endl;
	mat.release();
}
