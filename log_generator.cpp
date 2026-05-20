#include <iostream>
#include <winsock2.h>
#include <ws2tcpip.h>

#pragma comment(lib, "ws2_32.lib")

#define SERVER_PORT 9090

using namespace std;

int main() {

    WSADATA wsaData;
    SOCKET clientSocket;
    sockaddr_in serverAddr;

    WSAStartup(MAKEWORD(2,2), &wsaData);

    clientSocket = socket(AF_INET, SOCK_STREAM, 0);

    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(SERVER_PORT);
    serverAddr.sin_addr.s_addr = inet_addr("127.0.0.1");

    if (connect(clientSocket, (sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        cout << "Connection failed." << endl;
        return 1;
    }

    cout << "Connected to server." << endl;

    while (true) {

        string level, category, service, component, message;

        cout << "\nEnter Log Level (or EXIT): ";
        getline(cin, level);
        if (level == "EXIT") break;

        cout << "Enter Category: ";
        getline(cin, category);

        cout << "Enter Service: ";
        getline(cin, service);

        cout << "Enter Component: ";
        getline(cin, component);

        cout << "Enter Message: ";
        getline(cin, message);

        string logData = level + "|" + category + "|" + service + "|" + component + "|" + message;

        send(clientSocket, logData.c_str(), logData.length(), 0);
    }

    closesocket(clientSocket);
    WSACleanup();
    return 0;
}