#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <iostream>
#include <QFileDialog>
#include <QString>
#include <QFile>
#include <QTextStream>
#include <QImage>
#include <qdebug.h>
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>

using namespace std;
using namespace cv;

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_pushButton_openimage_clicked()
{
    QString filePath = QFileDialog::getOpenFileName(this,tr("Open File"),"",tr("image(*.png *.jpeg *.jpg)"));
    string fileName = filePath.toStdString();
    //string fileName = "C:\\Users\\BERLIN CHEN\\Desktop\\DDLAB\\PRO\\OpenCV_HW2\\rice.jpg";
    cout << fileName;
    Mat img,kernal_di,kernal_er;
    img = imread(fileName);
    Mat img_orig = img.clone();
    Mat img_marked = img.clone();

    cvtColor(img,img,COLOR_RGB2GRAY);
    cv::threshold(img,img,143,255,THRESH_BINARY_INV);
    Mat img_bi = img.clone();

    Mat kernel_di = getStructuringElement(MORPH_RECT,Size(7,7));
    cv::dilate(img,img,kernel_di);
    Mat img_di = img.clone();

    Mat kernel_er = getStructuringElement(MORPH_RECT,Size(31,31));
    cv::erode(img,img,kernel_er);
    Mat img_er = img.clone();

    cvtColor(img_bi,img_bi,COLOR_GRAY2RGB);
    cvtColor(img_di,img_di,COLOR_GRAY2RGB);
    cvtColor(img_er,img_er,COLOR_GRAY2RGB);

    Mat up;
    hconcat(img_orig,img_bi,up);

    Mat down;
    hconcat(img_di,img_er,down);

    Mat display;
    vconcat(up,down,display);

    cv::resize(display,display,Size(960,640));
    imshow("process",display);

    vector<vector<Point>> contours;
    vector<Vec4i> hierarchy;

    findContours(img,contours,hierarchy,RETR_TREE,CHAIN_APPROX_SIMPLE,Point());
    QString qnum = QString::number(contours.size());
    string num = qnum.toStdString();

    qDebug() << contours.size();
    Mat imgContours = Mat::zeros(img.size(),CV_8UC1);
    for(int i=0;i<contours.size();i++){
        drawContours(imgContours,contours,i,Scalar(255),1,8,hierarchy);
        drawMarker(imgContours,contours[i][0],Scalar(255,0,0));
        drawMarker(img_marked,contours[i][0],Scalar(0,0,0),10,2,12);
        cv::putText(img_marked,num,Point(800,800),cv::FONT_HERSHEY_SIMPLEX,2,Scalar(0, 0, 0), 4, 18, 0);
    }

    imshow("contours",imgContours);
    imshow("marked",img_marked);

    waitKey(0);

}

