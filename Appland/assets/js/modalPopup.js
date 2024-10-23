// 모달 생성 함수
function createModal(value) {

    //기존 모달이 있는경우 삭제
    const existingModal = document.querySelector('.popup-wrap');
    if (existingModal) {
        existingModal.remove();
    }

    // 모달 요소를 생성
    const modalWrap = document.createElement('div');
    modalWrap.classList.add('popup-wrap'); // 기본적으로 보이지 않음
    let modalContent = ``
    switch (value) {
        case "errFile": modalContent = `
            <div class="popup">
            <div class="popup-head">
                <h1>확장자 에러</h1>
            </div>
            <div class="popup-body">
                <img src="./assets/img/modalIcon/errFile.png"><br>
                <p>지원되지 않는 확장자입니다.</p>
            </div>
            <div class="popup-foot">
                <div class="pop-btn" id="confirm">확인</div>
            </div>
            </div>
        `; break;
        case "overFileSize": modalContent = `
            <div class="popup">
            <div class="popup-head">
                <h1>파일 크기 초과</h1>
            </div>
            <div class="popup-body">
                <img src="./assets/img/modalIcon/overFileSize.png"><br>
                <p>파일 크기가 너무 큽니다.</p>
            </div>
            <div class="popup-foot">
                <div class="pop-btn" id="confirm">확인</div>
            </div>
            </div>
        `; break;

        default: modalContent = `
            <div class="popup">
            <div class="popup-head">
                <h1>Error</h1>
            </div>
            <div class="popup-body">
                <img src="./assets/img/modalIcon/default.png"><br>
                <p>에러가 발생했습니다. <br>잠시후 다시 이용해주세요.</p>
            </div>
            <div class="popup-foot">
                <div class="pop-btn" id="confirm">확인</div>
            </div>
            </div>
        `
            break;
    }



    // 모달 내부 HTML 추가
    modalWrap.innerHTML = modalContent;

    // 모달을 body에 추가
    document.body.appendChild(modalWrap);

    // 모달을 서서히 나타나게 함
    setTimeout(() => {
        modalWrap.classList.add('show');
        modalWrap.style.display = 'flex'; // 모달을 보이게 함
    }, 10);

    

    // 확인 버튼 클릭 시 모달 닫기
    document.getElementById('confirm').addEventListener('click', () => {
        closeModal(modalWrap);
    });
}

// 모달 닫기 함수
function closeModal(modalWrap) {
    modalWrap.classList.add('hide'); // 서서히 사라지게 함
    modalWrap.classList.remove('show'); // show 클래스를 제거

    // 애니메이션이 끝난 후 display를 none으로 설정
    modalWrap.addEventListener('transitionend', () => {
        modalWrap.style.display = 'none';
        modalWrap.remove(); // DOM에서 완전히 제거
    }, { once: true }); // transitionend 이벤트는 한 번만 발생하도록 설정
}

// 모달 열기 버튼 이벤트 리스너
document.getElementById('modal-open').addEventListener('click', function () {
    createModal("");
});
