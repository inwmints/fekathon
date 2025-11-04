class BuildingNavigator {
    constructor() {
        this.currentFloor = 1;
        this.floorPlans = {};
        this.canvas = document.getElementById('floor-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.currentHighlight = null;
        
        this.initializeEventListeners();
        this.loadFloorPlans();
        this.initializeSmokingWarning();
    }

    initializeSmokingWarning() {//сообщение при входе
        setTimeout(() => {
            this.showSmokingWarning();
        }, 1000);

        this.smokingWarningInterval = setInterval(() => {//каждые 2-5 минут
            this.showSmokingWarning();
        }, Math.floor(Math.random() * (300000 - 120000 + 1)) + 120000); // 2-5 минут
    
    }

    showSmokingWarning() {//сообщение о курении
        alert("🚭 Запрет курения\n\nКурение табака запрещено на территории всего колледжа, рядом с ним и прокуратурой");
    }

    initializeEventListeners() { //ввод кабинета
        document.getElementById('search-btn').addEventListener('click', () => {
            this.searchRoom();
        });

        document.getElementById('room-number').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.searchRoom();
            }
        });


        document.querySelectorAll('.floor-btn').forEach(btn => {//выбор этажа
            btn.addEventListener('click', (e) => {
                this.switchFloor(parseInt(e.target.dataset.floor));
            });
        });
    }

    async loadFloorPlans() {//загрузка этажей
        const floors = [1, 2, 3, 4];
        const loadPromises = floors.map(floor => this.loadFloorImage(floor));
        
        try {
            await Promise.all(loadPromises);
            this.displayFloorPlan();
        } catch (error) {
            this.showNoImageMessage();
        }
    }

    loadFloorImage(floorNumber) {//вывод выбранного этажа
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => {
                this.floorPlans[floorNumber] = {
                    image: img,
                    name: `f${floorNumber}`
                };
                resolve(img);
            };
            img.onerror = () => {
                console.warn(`Не удалось загрузить схему для этажа ${floorNumber}`);
                
            };
            
            img.src = `img/f${floorNumber}.png`;
            
            setTimeout(() => {
                if (!img.complete || typeof img.naturalWidth === "undefined" || img.naturalWidth === 0) {
                    img.src = `img/f${floorNumber}.jpg`;
                }
            }, 100);
        });
    }

    displayFloorPlan() {
        const floorData = this.floorPlans[this.currentFloor];
        if (!floorData || !floorData.image) {
            this.showNoImageMessage();
            return;
        }

        const img = floorData.image;
        const canvas = this.canvas;

        canvas.width = img.width;
        canvas.height = img.height;
        
        this.ctx.clearRect(0, 0, canvas.width, canvas.height);
        this.ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

        this.drawAllRooms();

        canvas.style.display = 'block';
        document.getElementById('no-image-message').style.display = 'none';
    }

    drawAllRooms() {//поиск кабинетов в массив и их координат
        const floorIndex = this.currentFloor - 1;
        
        if (buildingStructure[floorIndex]) {
            buildingStructure[floorIndex].forEach((wing, wingIndex) => {
                wing.forEach(roomNumber => {
                    const roomDetail = roomDetails[roomNumber];
                    if (roomDetail) {
                        this.drawRoom({
                            number: roomNumber,
                            x: roomDetail.x,
                            y: roomDetail.y,
                            type: roomDetail.type
                        }, false);
                    }
                });
            });
        }

        if (this.currentHighlight) {
            this.drawRoom(this.currentHighlight, true);
        }
    }

    drawRoom(room, isHighlighted = false) {//просто отрисовка
        const x = room.x * this.canvas.width;
        const y = room.y * this.canvas.height;
        
        if (isHighlighted) {
            this.ctx.beginPath();
            this.ctx.arc(x, y, 27, 0, 2 * Math.PI);
            this.ctx.fillStyle = 'rgba(255, 215, 0, 0.3)';
            this.ctx.fill();
            this.ctx.strokeStyle = 'gold';
            this.ctx.lineWidth = 3;
            this.ctx.stroke();

            this.ctx.fillStyle = 'orange';
            this.ctx.font = 'bold 24px Arial';
            this.ctx.textAlign = 'center';
            this.ctx.textBaseline = 'middle';
            this.ctx.fillText(room.number, x, y);
        } else {
            this.ctx.fillStyle = '#3498db';
            this.ctx.beginPath();
            this.ctx.arc(x, y, 25, 0, 2 * Math.PI);
            this.ctx.fill();
            
            

            this.ctx.fillStyle = 'white';
            this.ctx.font = '24px Arial';
            this.ctx.textAlign = 'center';
            this.ctx.textBaseline = 'middle';
            this.ctx.fillText(room.number, x, y);
        }
    }


    
    showNoImageMessage() {
        document.getElementById('no-image-message').style.display = 'block';
        this.canvas.style.display = 'none';
        
        const messageElement = document.getElementById('no-image-message');
        messageElement.innerHTML = 'Схема для этажа ' + this.currentFloor + ' не найдена.<br>Разместите файлы f1.png, f2.png, f3.png, f4.png в папке "img"';
    }

    switchFloor(floorNumber) {
        this.currentFloor = floorNumber;
        this.currentHighlight = null;
        
        document.querySelectorAll('.floor-btn').forEach(btn => {
            btn.classList.remove('active');
            if (parseInt(btn.dataset.floor) === floorNumber) {
                btn.classList.add('active');
            }
        });

        this.displayFloorPlan();
    }

    searchRoom() {
        const roomNumber = document.getElementById('room-number').value.trim();
        console.log('Поиск кабинета:', roomNumber);
        
        if (!roomNumber) {
            alert('Введите номер кабинета');
            return;
        }

        const roomLocation = findRoomInStructure(roomNumber);
        console.log('Результат поиска:', roomLocation);
        
        if (!roomLocation.exists) {
            alert(`Кабинет ${roomNumber} не найден в здании`);
            return;
        }

        if (roomLocation.floor !== this.currentFloor) {
            this.switchFloor(roomLocation.floor);
        }

        this.showRoomInfo(roomNumber, roomLocation);
    }

    showRoomInfo(roomNumber, location) {
        console.log('showRoomInfo вызван с:', roomNumber, location);
        
        const roomInfo = document.getElementById('room-info');
        const roomDetailsElement = document.getElementById('room-details');
        
        const roomDetail = roomDetails[roomNumber];
        console.log('Детали кабинета:', roomDetail);
        
        if (!roomDetail) {
            roomDetailsElement.innerHTML = `
                <strong>Кабинет ${roomNumber}</strong><br>
                Информация о кабинете отсутствует<br>
                <strong>Расположение:</strong> ${location.floor} этаж, ${location.wingName}
            `;
        } else {
            roomDetailsElement.innerHTML = `
                <strong>Кабинет ${roomNumber}</strong><br>
                ${roomDetail.description}<br>
                <strong>Расположение:</strong> ${location.floor} этаж, ${location.wingName}<br>
                
            `;
        }
        
        roomInfo.classList.remove('hidden');
        console.log('Информация о кабинете должна быть видна');
        
        this.highlightRoom(roomNumber, roomDetail || { x: 0.5, y: 0.5, type: 'classroom' });
        
        document.getElementById('room-number').value = '';
        document.getElementById('room-number').focus();
    }

    highlightRoom(roomNumber, roomDetail) {
        this.currentHighlight = {
            number: roomNumber,
            x: roomDetail.x,
            y: roomDetail.y,
            type: roomDetail.type
        };
        this.displayFloorPlan();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new BuildingNavigator();
});