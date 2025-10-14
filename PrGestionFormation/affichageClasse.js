// affichageClasse.js

let classrooms = [];
let roomCounter = 0;

function ajouterClasse(id, name, students, desksPerRow, layout) {
    classrooms.push({ id, name, students, desksPerRow, layout });
    renderSchool();
    updateSummary();
}

function renderSchool() {
    const rowContainer = document.getElementById('classRow');
    if (!rowContainer) return;
    rowContainer.innerHTML = '';
    classrooms.forEach(classroom => {
        const col = document.createElement('div');
        col.className = 'col-12 col-md-6';
        col.appendChild(createClassroomRoom(classroom));
        rowContainer.appendChild(col);
    });
}

function createClassroomRoom(classroom) {
    const room = document.createElement('div');
    room.className = 'card mb-4';
    room.innerHTML = `
        <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
            <span class="fw-bold">${classroom.name}</span>
            <span class="badge bg-light text-dark">${classroom.students} élèves</span>
        </div>
        <div class="card-body">
            <div class="mb-3 text-center fw-bold">TABLEAU</div>
            <div class="row" id="desks-${classroom.id}"></div>
        </div>
    `;
    setTimeout(() => renderClassroomLayout(classroom), 100);
    return room;
}

function renderClassroomLayout(classroom) {
    const container = document.getElementById(`desks-${classroom.id}`);
    if (!container) return;
    container.innerHTML = '';
    if (classroom.layout === 'rows') {
        generateRowsLayout(container, classroom.students, classroom.desksPerRow);
    } else if (classroom.layout === 'circle') {
        generateCircleLayout(container, classroom.students);
    }
}

function generateRowsLayout(container, students, desksPerRow) {
    const numRows = Math.ceil(students / desksPerRow);
    let studentNum = 1;
    for (let row = 0; row < numRows; row++) {
        const rowDiv = document.createElement('div');
        rowDiv.className = 'desk-row';
        const desksInRow = Math.min(desksPerRow, students - (row * desksPerRow));
        for (let i = 0; i < desksInRow; i++) {
            rowDiv.appendChild(createMiniDesk(studentNum++));
        }
        container.appendChild(rowDiv);
    }
}

function generateCircleLayout(container, students) {
    const circleDiv = document.createElement('div');
    circleDiv.className = 'circle-layout';
    const radius = Math.min(70, 30 + students * 2);
    const angleStep = (2 * Math.PI) / students;
    for (let i = 0; i < students; i++) {
        const angle = i * angleStep - Math.PI / 2;
        const x = radius * Math.cos(angle);
        const y = radius * Math.sin(angle);
        const desk = createMiniDesk(i + 1);
        desk.style.position = 'absolute';
        desk.style.left = `calc(50% + ${x}px - 14px)`;
        desk.style.top = `calc(50% + ${y}px - 14px)`;
        circleDiv.appendChild(desk);
    }
    container.appendChild(circleDiv);
}

function createMiniDesk(studentNum) {
    const desk = document.createElement('div');
    desk.className = 'desk-mini';
    desk.title = `Élève ${studentNum}`;
    const student = document.createElement('div');
    student.className = 'student-mini';
    desk.appendChild(student);
    return desk;
}

function updateSummary() {
    // Optionnel : à adapter selon tes besoins
}
