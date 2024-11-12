# Vietnam_traffic_signs_recognition <br>
## Chạy trên google colab: <br>
Bản chạy demo trên colab về traffic_signs_recognition: https://drive.google.com/file/d/11REaOAQi_f-Rhon5hM6YHWYnoFqy6gBl/view?usp=sharing <br>
Bộ dataset https://drive.google.com/file/d/14qiArH8PzWMAf1YA4x6951y6-rFxAJ6V/view?usp=drive_link <br>
## Chạy trên máy ảo conda: <br>
Git clone yolov5 về máy: https://github.com/ultralytics/yolov5 <br>
Mở conda và chạy: pip install -r requirements.txt để cài đặt thư viện cho yolov5 <br>
<details open>
<summary>  Train  </summary>
Dùng lệnh để chạy lệnh train: python /path/to/train.py --img 640 --batch 3 --epochs 50 path/to/file/yaml.data --weights path/to/file/yolov5s.pt --cache <br>
  <br>
-path/to/train.py: nằm trong file yolov5 sau khi đã tải về. <br>
-img: kích thước ảnh, batch: batch size, epochs: số epochs muốn train. <br>
-path/to/file/yaml.data: trỏ đến thư mục train và valid của bộ data, đồng thời chứa các label của bộ data. <br>
-weights: file chứa trọng số để train. Tải file yolov5s.pt để làm trọng số ban đầu. Sau lần train đầu tiên sẽ lưu lại best.pt và last.pt từ đó chọn trọng số phù hợp cho lần train tiếp theo. <br>
-Sau mỗi lần train trong file yolov5/runs/train sẽ tự generate 1 file exp sẽ chứa các thông số sau khi train báo gồm: weights, confusion_matrix, F1_curve, labels, labels_correlogram, P_curve, PR_curve, R_curve, results.csv, results.img và các imgs batched file. <br>
</details>

<details open>
<summary>  Detect  </summary> 
Sau khi train xong dùng lệnh sau để test: python /detect path/to/detect.py --weights /path/to/best.pt --img 640 --conf 0.1 --source /path/to/test <br>
  <br>
-path/to/test: nơi chứa các file test. <br>
-path/to/best.pt: bộ trọng số sau khi đã được học dùng và được sử dụng để detect ảnh test. <br>
-detect path/to/detect.py: file detect trong yolov5. <br>
-Sau mỗi lần detect trong file yolov5/runs/detect sẽ tự generate 1 file exp sẽ lưu lại toàn bộ kết quả dự đoán.  <br>       
</details>

<details open>
<summary> Deployment  </summary>
File server.py được dùng để deploy lên local host. Có thể thay đổi đường dẫn các file cho phù hợp và chỉnh port nếu cần thiết.
Pip install -r requirements.txt cho file server.py
