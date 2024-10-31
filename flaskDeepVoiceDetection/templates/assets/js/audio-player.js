//파일명: audio-player.js
document.addEventListener("DOMContentLoaded", function () {
    const audioPlayer = document.getElementById("audio-player");
    const playButton = document.querySelector(".play-button");
    const rewindButton = document.querySelector(".rewind-button");
    const forwardButton = document.querySelector(".fast-forward-button");
    const backButton = document.querySelector(".back-button");
    const skipButton = document.querySelector(".skip-button");
    const progressBar = document.querySelector(".progress-bar");
    const progressWrapper = document.querySelector(".progress-bar-wrapper");
    const currentTimeDisplay = document.querySelector(".progress-time-current");
    const totalTimeDisplay = document.querySelector(".progress-time-total");
    const playButtonImg = document.getElementById("fa-playImg");
  
    // 음악 재생 및 일시정지
    playButton.addEventListener("click", () => {
      if (audioPlayer.paused) {
        audioPlayer.play();
        playButton.querySelector("i").classList.replace("fa-play", "fa-pause");
        playButtonImg.src = "./assets/img/audioBtn/pause.png";
      } else {
        audioPlayer.pause();
        playButton.querySelector("i").classList.replace("fa-pause", "fa-play");
        playButtonImg.src = "./assets/img/audioBtn/play.png";
      }
    });
  
    // 처음으로 이동 (back 버튼)
    backButton.addEventListener("click", () => {
      audioPlayer.currentTime = 0;
    });
  
    // 5초 뒤로 이동 (rewind 버튼)
    rewindButton.addEventListener("click", () => {
      audioPlayer.currentTime = Math.max(0, audioPlayer.currentTime - 5);
    });
  
    // 5초 앞으로 이동 (fast forward 버튼)
    forwardButton.addEventListener("click", () => {
      audioPlayer.currentTime = Math.min(audioPlayer.duration, audioPlayer.currentTime + 5);
    });
  
    // 끝으로 이동 (skip 버튼)
    skipButton.addEventListener("click", () => {
      audioPlayer.currentTime = audioPlayer.duration;
    });
  
    // 음악 재생 시간 업데이트 (progress bar와 시간 표시 업데이트)
    audioPlayer.addEventListener("timeupdate", () => {
      const progressPercentage = (audioPlayer.currentTime / audioPlayer.duration) * 100;
      progressBar.style.width = `${progressPercentage}%`;
  
      // 현재 재생 시간과 총 재생 시간을 표시
      currentTimeDisplay.textContent = formatTime(audioPlayer.currentTime);
      totalTimeDisplay.textContent = formatTime(audioPlayer.duration);
    });
  
    // 음악의 총 재생 시간이 준비되면 totalTime 표시
    audioPlayer.addEventListener("loadedmetadata", () => {
      totalTimeDisplay.textContent = formatTime(audioPlayer.duration);
    });
  
    // 진행 바 클릭 시 재생 시간을 이동시키는 이벤트
    progressWrapper.addEventListener("click", (event) => {
      const rect = progressWrapper.getBoundingClientRect(); // 진행 바의 위치와 크기 정보
      const clickX = event.clientX - rect.left; // 클릭한 위치의 X 좌표
      const width = rect.width; // 진행 바의 전체 너비
      const duration = audioPlayer.duration; // 오디오의 총 길이
  
      // 클릭한 위치에 해당하는 시간으로 오디오의 현재 시간을 변경
      const newTime = (clickX / width) * duration;
      audioPlayer.currentTime = newTime;
    });
  
    // 시간을 포맷하는 함수 (초를 분:초로 변환)
    function formatTime(time) {
      const minutes = Math.floor(time / 60);
      const seconds = Math.floor(time % 60);
      return `${minutes}:${seconds.toString().padStart(2, "0")}`;
    }
  });
  