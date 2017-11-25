#include <opencv2/imgproc/imgproc.hpp>

class TargetProc {
	private:
	int round2(double a) {
		if(a < 0) {
			a -= 0.5;
		} else if(a > 0) {
			a += 0.5;
		}
		return (int) a;
	}
	public:
	void procTarget(cv::Mat &img, cv::vector<cv::vector<cv::Point> > &contours, Networking networking) {
		cv::vector<cv::Point> largestContour = contours[0];
		cv::vector<cv::Point> secondLargestContour = contours[1];

		std::cout << "Number of contours: " << contours.size() << "\n";	
		cv::Scalar color(0, 225, 0);
		cv::drawContours(img, contours, -1, color, CV_FILLED);
		cv::Rect rect;
		rect = cv::boundingRect(largestContour);
		double hpx = rect.size().height;		
		std::cout << "Height: " << hpx << "\n";
		double distance = (480*5.08)/(2*hpx*tan(0.726/2));
		std::cout << "Distance: " << distance << "\n";
		cv::Moments moments = cv::moments(largestContour);
		if(moments.m00 == 0) {
			std::cout << "Invalid moments!\n";
			return;
		} 
		int cx = round2(moments.m10/moments.m00);
		int cy = round2(moments.m01/moments.m00);
		std::cout << "(" << cx << ", " << cy << ")\n";
		cv::Moments moments2 = cv::moments(secondLargestContour);
		if(moments2.m00 == 0) {
			std::cout << "Invalid moments!\n";
			return;
		} 
		int cx2 = round2(moments2.m10/moments2.m00);
		int cy2 = round2(moments2.m01/moments2.m00);
		std::cout << "(" << cx2 << ", " << cy2 << ")\n";
		double pegx = (cx+cx2)/2;
		double angle = atan(5.08*(pegx-320)/(hpx*distance));
		std::cout << "Angle: " << angle << "\n";
		networking.senddouble(angle);
	}
};


