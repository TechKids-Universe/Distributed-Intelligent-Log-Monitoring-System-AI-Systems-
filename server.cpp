#include <iostream>
#include <thread>
#include <winsock2.h>
#include <ws2tcpip.h>

#pragma comment(lib, "ws2_32.lib")

#define SERVER_PORT 9090
#define AI_ENGINE_PORT 9091

using namespace std;

void handleClient(SOCKET clientSocket, string clientIP) {

    char buffer[1024];

    while (true) {

        int bytesReceived = recv(clientSocket, buffer, sizeof(buffer), 0);
        

        if (bytesReceived <= 0)
            break;

        buffer[bytesReceived] = '\0';
        string logData(buffer);

        cout << "From [" << clientIP << "]: " << logData << endl;

        // Forward to AI Engine (include client IP)
        SOCKET aiSocket = socket(AF_INET, SOCK_STREAM, 0);

        sockaddr_in aiAddr;
        aiAddr.sin_family = AF_INET;
        aiAddr.sin_port = htons(AI_ENGINE_PORT);
        aiAddr.sin_addr.s_addr = inet_addr("127.0.0.1");

        if (connect(aiSocket, (sockaddr*)&aiAddr, sizeof(aiAddr)) != SOCKET_ERROR) {

            string finalData = clientIP + "|" + logData;
            send(aiSocket, finalData.c_str(), finalData.length(), 0);
        }

        closesocket(aiSocket);
    }

    closesocket(clientSocket);
    cout << "Client disconnected: " << clientIP << endl;
}

int main() {

    WSADATA wsaData;
    SOCKET serverSocket;
    sockaddr_in serverAddr;

    WSAStartup(MAKEWORD(2,2), &wsaData);

    serverSocket = socket(AF_INET, SOCK_STREAM, 0);

    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(SERVER_PORT);
    serverAddr.sin_addr.s_addr = INADDR_ANY;

    bind(serverSocket, (sockaddr*)&serverAddr, sizeof(serverAddr));
    listen(serverSocket, SOMAXCONN);

    cout << "Multi-client Server Started..." << endl;

    while (true) {

        sockaddr_in clientAddr;
        int clientSize = sizeof(clientAddr);

        SOCKET clientSocket = accept(serverSocket, (sockaddr*)&clientAddr, &clientSize);

        char clientIP[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &clientAddr.sin_addr, clientIP, INET_ADDRSTRLEN);

        thread t(handleClient, clientSocket, string(clientIP));
        t.detach();
    }

    WSACleanup();
    return 0;
}