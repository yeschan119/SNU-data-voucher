# image segmentation 및 annotation 프로젝트
## 서울대학교 데이터 가공/처리 프로젝트

## Purpose
  + image segmentation 및 annotation
  + pytorch를 이용한 semantic segmentation을 진행
  + segmentation이 끝난 데이터에서 annotation 결과 추출
  + 자동 segmentation으로 생긴 오류값들을 검사하고 제거하여 완벽한 annotation 결과 도출
  
## 👨‍👦Members
  + 김범진
  + 강응찬
  
## Tech
  + OpenCV
  + sementic segmentation
  + image annotation
  + xml
  + docker

## Project Plan
  + 9월 8일 담당자와 인터뷰 및 샘플 데이터 수령
  + 9월 15일까지 샘플데이터를 이용한 script 개발
  + 9월 17일 결과물을 사업부에 공유 및 피드백
  + 9월 20일 전체 데이터 수령(약 5만장)
  + 9월 30일까지 script 완료
  + 10얼 15일까지 모델 완성하고 전체 데이터를 가공하여 사업부에 넘기기

## 첫 주 [Time Table]
  + 요구사항 충분히 분석
  + annotation points에 대한 데이터 전처리 작업
  + image annotaion viewer 만들기
  + 필요한 알고리즘이나 기술들 정리해보기

+ ## 9월 8일
  + 샘플데이터를 받아 분석 진행
  + openCV, tkinter 를 이용한 image annotation viewer 제작 50% 완료
  + XML형식의 annotaiont points에 대한 전처리 작업 진행
  + 사용한 모듈 및 스킬
    + XML parsing에서 .tag .attrib .text 이용
    + list 사이즈를 줄이기 위해 List[1::2] 사용
    + image를 처리하기 위해 openCV 모듈 사용
    + cv2.imread() cv2.resize() cv2.imshow() cv2.waitKey() cv2.destropy()
    + tkinter 객체에 openCV로 만든 image파일 넣어서 출력하기
    + openCV는 BGR순서로 색깔을 표시하기에 이것부터 RGB로 바꾸어야 한다.  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    + 바꾼 후 tkinter 차의 크기에 맞추어야 하므로 사이즈 변경(꼭 상대사이즈로 변경!!)
    + cv2.resize(self.img1, dsize = (0,0), fx = 0.35, fy = 0.35, interpolation = cv2.INTER_LINEAR)
    + openCV는 numpy 타입의 데이터이므로 이를 img타입으로 바꾸어야 tkinter에 사용 가능 Image.fromarray(self.img2)
    + 다음 두 식을 통해 tkinter에서 이미지로 출력 완성
    + imgtk2 = ImageTk.PhotoImage(image=self.img2)
    + label1 = tk.Label(self.window, image=imgtk1)
    
+ ## 9월 9일
  + image annotation viewer 완성
  + tkinter에서 이미지와 이미지 이름을 한번에 받기
    + 실행 코드
     ```
     image_formats = [("JPEG","*.jpg")]
     file_path_list = askopenfilenames(filetypes=image_formats, initialdir="/", title='Please select a picture to analyze')
     ```
  + 서로 다른 annotation작업을 한 두 이미지를 한 화면에 출력
    + 중요한 코드(class에서 작업할 때 이 코드가 없으면 이미지 출력이 안 됨)
     ```
     label = tk.Label(self.window, image=imgtk2)
     label.image = imgtk2
     ```
  + 버튼을 누를 때마다 다른 이미지 출력
    + 한 화면에서 이미지가 바뀌기 위해 필요한 코드
    ```
    label1.config(image=imgtk1)
    ```
  + annotation이 더 잘 보이도록 masking 처리
    + 이미지롤 하나 더 복사
    + 복사한 이미지를 색깔로 채우기
    + 두 개의 이미지르 합치면서 복사한 이미지의 투명도를 정하기
    ```
    masked_img = cv2.fillPoly(masked_img, [pts], color)
    masked_img = cv2.addWeighted(masked_img, 0.6, img1, 1, 0)
    ```
  + x,y 좌표값으 조절해서 annotation 결과에 대한 실험 진행
    + 각각의 polygon 에서 x,y 좌표를 따로 추출하여 평균값 구하기
    + 평균값보다 큰 x,y는 값을 줄이고 작은 x,y는 값을 늘리는 방식으로 설계
    + 구현 결과 어느 정도 성과는 보았으나 만족한 결과는 아님
    
+ ## 9월 13일
  + choose another way to reduce polygon size.
  + modify the design of the gui to show several results.
  + use two ideas to reduce and smoothe edges.
    + get relative axis for each polygon and reduce using this.
    + get degree for every three points in a polygon and remove points having a small degree.
    
  + following is to reduce polygon size using relative axis for each polygon.
    + get max, min points to build a rectangle covering polygon.
    + get ratio x axis and y axis after building a rectangle.
    + define how many size should be reduced.
    + get relative points for every poings in the polygon.
    + reduce total size.
    
  + following code is to get degree to prune edges.
    + get degrees for every three points.
    + if a degree is smaller than 30 or 40.., the point is removed.
    ```
    from math import atan2, degrees
    def angle_between_three_points(self, points):
        x1, y1 = points[0]
        x2, y2 = points[1]
        x3, y3 = points[2]
        deg1 = (360 + degrees(atan2(x1 - x2, y1 - y2))) % 360
        deg2 = (360 + degrees(atan2(x3 - x2, y3 - y2))) % 360
        return deg2 - deg1 if deg1 <= deg2 else 360 - (deg1 - deg2)
    ```
 
+ ## 9월 15
  + make download xml function.
  + reduce time complexity with half(40s -> 12S).
  + finish script for sample data

+ ## 9월 30일
  + 전체 데이터 전달 받음
  + semantic-segmentation과 관련된 논문 검색
  + MIT에서 제공하는 pytorch를 이용한 semantic-segmentation 코드에 대한 테스팅 진행
    + github 주소
    ```
    https://github.com/CSAILVision/semantic-segmentation-pytorch
    ```
+ ## 10월 첫주
  + semantic-segmentation 코드를 현재 프로젝트에 맞게 수정
  + 수정한 코드를 이용하여 4만 객체에 대한 segmentation 진행
  + 자동 segmentation을 통해 생기는 오류값들에 대한 처리 진행
  + 전체 이미지에 대한 segmentation 및 annotation을 완료하여 전달
