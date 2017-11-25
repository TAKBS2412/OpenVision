#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

class Networking {
	
	private:
	int sockfd, portno, n;
	struct sockaddr_in serv_addr;
	struct hostent *server;

	void error(const char *msg)
	{
		perror(msg);
		exit(0);
	}
	
	public:
	Networking(const char* hostname, int port) {
		portno = port;
		sockfd = socket(AF_INET, SOCK_STREAM, 0);
		if (sockfd < 0)
			error("ERROR opening socket");
		server = gethostbyname(hostname);
		if (server == NULL) {
			fprintf(stderr,"ERROR, no such host\n");
			exit(0);
		}
		bzero((char *) &serv_addr, sizeof(serv_addr));
		serv_addr.sin_family = AF_INET;
		bcopy((char *)server->h_addr,
			 (char *)&serv_addr.sin_addr.s_addr,
			 server->h_length);
		serv_addr.sin_port = htons(portno);
		if (connect(sockfd,(struct sockaddr *) &serv_addr,sizeof(serv_addr)) < 0)
			error("ERROR connecting");
	}

	int senddouble(double data)
	{
		char buffer[256];
		char oldbuffer[256];
		bzero(buffer,256);
		int num = sprintf(buffer, "%f\n", data);
		if (num > 256) 
			error("ERROR, data too large!");
		strncpy(oldbuffer, buffer, 256);
		n = write(sockfd,buffer,strlen(buffer));
		if (n < 0)
			error("ERROR writing to socket");
		bzero(buffer,256);
		/*
		n = read(sockfd,buffer,255);
		if (n < 0)
			error("ERROR reading from socket");
		printf("%s\n",buffer);
		*/
		return 0;
	}

	void closeSocket() {
		close(sockfd);
	}
};
/*
int main() {
	char hostname[] = "192.168.0.10";
	Networking networking = Networking(hostname, 2412);
	networking.senddouble(948);
	networking.senddouble(2412);
	networking.closeSocket();
	return 0;
}
*/
