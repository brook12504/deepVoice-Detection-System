//파일명: assets/js/input-page-dropbox.js

var input = document.getElementById("input");
var initLabel = document.getElementById("label");
var inner = document.getElementById("inner");
var originalInnerHTML = inner.innerHTML; // 초기 상태 저장
var originalLabelBg = initLabel.style.backgroundImage; // 라벨의 원래 배경
var audioPlayer = document.getElementById("audio-player"); // 오디오 플레이어
var mediaControls = document.querySelector(".media-controls"); // 미디어 컨트롤 요소

input.addEventListener("change", (event) => {
    const files = changeEvent(event);
    if (files.length > 0) {
        handleFileUpload(files[0]);
    }

    // 파일이 선택된 후 input 값을 초기화
    input.value = ''; // 이렇게 하면 동일한 파일을 다시 선택할 수 있습니다.
});

function handleFileUpload(file) {
    const allowedExtensions = ['mp3', 'm4a', 'aac', 'wav']; // 허용된 확장자 목록
    const maxFileSize = 30 * 1024 * 1024; // 30MB

    const fileName = file.name;
    const fileExtension = fileName.split('.').pop().toLowerCase(); // 파일 확장자 추출
    const fileSize = file.size; // 파일 크기 추출

    // 1. 확장자 체크
    if (!allowedExtensions.includes(fileExtension)) {
        createModal("errFile"); // 확장자가 허용되지 않으면 모달 표시
        return;
    }

    // 2. 파일 크기 체크
    if (fileSize > maxFileSize) {
        createModal("overFileSize"); // 파일 크기가 30MB 이상이면 모달 표시
        return;
    }

    // 확장자와 파일 크기 모두 유효한 경우에만 파일 처리
    const filePath = URL.createObjectURL(file);

    let displayName = fileName;
    if (displayName.length > 25) {
        const baseName = displayName.slice(0, 20);  // 앞 20글자 추출
        const remainingName = displayName.slice(displayName.lastIndexOf('.'));  // 확장자 추출
        displayName = `${baseName} • • •${remainingName}`;  // 이름을 ' • • • '로 대체하고 확장자 추가
    }

    // 기존 inner 내용 숨기기
    inner.innerHTML = ''; // 기존 내용을 지웁니다.

    // 파일 정보 텍스트 생성
    const fileInfo = document.createElement('p');
    fileInfo.innerText = `${displayName}\n`;
    fileInfo.classList.add('file-info'); // 중앙에 위치하는 클래스 적용
    fileInfo.style.fontWeight = "1000";
    fileInfo.style.fontSize = "28px";
    inner.appendChild(fileInfo);

    // 분석 시작 버튼 생성
    const analyzeBtn = document.createElement('button');
    analyzeBtn.innerText = "분석 시작";
    analyzeBtn.classList.add('analyze-btn'); // 하단 중앙에 위치하는 클래스 적용

    // 버튼에 마우스 호버 시 그라데이션 애니메이션 적용
    analyzeBtn.addEventListener('mouseover', () => {
        analyzeBtn.style.backgroundPosition = '0 0';
    });
    analyzeBtn.addEventListener('mouseout', () => {
        analyzeBtn.style.backgroundPosition = '200% 0';
    });

    // 버튼을 inner에 추가
    inner.appendChild(analyzeBtn);

    // 라벨 배경을 지정된 이미지로 변경
    initLabel.style.backgroundImage = 'url("/templates/assets/img/dropboxBackGroung_1.jpg")';
    initLabel.style.backgroundSize = 'cover';

    // 빛 반사 효과를 위한 클래스 추가
    initLabel.classList.add('uploaded');

    // 미디어 컨트롤 표시 및 오디오 파일 적용
    mediaControls.style.display = "flex";  // media-controls의 display 속성을 flex로 변경
    audioPlayer.src = filePath;  // 오디오 플레이어에 업로드된 파일 경로를 설정
    audioPlayer.load();  // 새로운 파일을 로드


    //분석 시작 버튼 클릭시 서버에게 post 전송
    analyzeBtn.addEventListener("click", async () => {
        createModal("fileUpload"); // 모달창 생성

        if (!file) {
            alert("음성 파일을 선택해 주세요.");
            return;
        }

        const formData = new FormData();
        formData.append("name", fileName); // 파일명 추가
        formData.append("audioFile", file); // 실제 파일 추가

        try {
            const response = await fetch("/upload", {
                method: "POST",
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                console.log("전송 성공:", result);

                // 서버로부터 받은 데이터를 localStorage에 저장
                localStorage.setItem('serverData', JSON.stringify(result));

                // output-page.html로 이동
                window.location.href = "/output-page";
            } else {
                console.error("전송 실패:", response.statusText);
            }
        } catch (error) {
            console.error("전송 중 오류 발생:", error);
        }
    });


}

// 기존 input 이벤트 리스너에 추가
input.addEventListener("change", (event) => {
    const files = changeEvent(event);
    if (files.length > 0) {
        handleFileUpload(files[0]);
    }
});

function resetToOriginal() {
    inner.innerHTML = originalInnerHTML;
    initLabel.style.backgroundImage = originalLabelBg;

    // 빛 반사 효과 클래스 제거
    initLabel.classList.remove('uploaded');
}

initLabel.addEventListener("mouseover", (event) => {
    event.preventDefault();
    const label = document.getElementById("label");
    label?.classList.add("label--hover");
});

initLabel.addEventListener("mouseout", (event) => {
    event.preventDefault();
    const label = document.getElementById("label");
    label?.classList.remove("label--hover");
});

document.addEventListener("dragenter", (event) => {
    event.preventDefault();
    console.log("dragenter");
    if (event.target.className === "inner") {
        event.target.style.background = "#d1d1d1";
        initLabel.style.backgroundColor = "#d1d1d1";
    }
});

document.addEventListener("dragover", (event) => {
    console.log("dragover");
    event.preventDefault();
});

document.addEventListener("dragleave", (event) => {
    event.preventDefault();
    console.log("dragleave");
    if (event.target.className === "inner") {
        event.target.style.background = "";
        initLabel.style.backgroundColor = "";
    }
});

document.addEventListener("drop", (event) => {
    event.preventDefault();
    console.log("drop");

    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
        handleFileUpload(files[0]); // 첫 번째 파일을 처리합니다.
    }

    // 드롭한 파일을 가져온 후 스타일을 원래 상태로 복구
    if (event.target.className === "inner") {
        event.target.style.background = "";
        initLabel.style.backgroundColor = "";
    }
});

// 파일 해제 시 초기 상태로 복귀
function resetToOriginal() {
    inner.innerHTML = originalInnerHTML;
    initLabel.style.backgroundImage = originalLabelBg;
}

// 파일 선택 취소 또는 해제 시 원래 상태로 복귀시키는 이벤트 추가
input.addEventListener("reset", resetToOriginal);

function changeEvent(event) {
    const { target } = event;
    return [...target.files];
}



