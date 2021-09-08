# SNU-data-voucher
서울대학교 데이터 가공/처리 프로젝트

## Purpose
  + image annotation
  + fine image -> coarse image

## Members

## Tech
  + OpenCV
  + image annotation
  + xml
  + docker

## Project Plan
  + 9월 8일 담당자와 인터뷰 및 샘플 데이터 수령
  + 9월 15일짜기 샘플데이터를 이용한 script 개발
  + 9월 17일 결과물을 사업부에 공유 및 피드백
  + 9월 20일 전체 데이터 수령(약 5만장)
  + 9월 30일까지 script 완료
  + 10얼 15일까지 모델 완성하고 전체 데이터를 가공하여 사업부에 넘기기

## 첫 주 [Time Table]
  + 요구사항 충분히 분석
  + annotation points에 대한 데이터 전처리 작업
  + image annotaion view 만들기
  + 필요한 알고리즘이나 기술들 정리해보기

+ ## 9월 9일
  + 예시 결과를 샘플로 받아 분석 진행
  + openCV, tkinter 를 이용한 image annotation view 제작 50% 완료
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
