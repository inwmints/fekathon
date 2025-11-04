
// Массив здания: [этаж][крыло][кабинет]
const buildingStructure = [
    // Этаж 0 (первый этаж)
    [
        ['101', '102', '103', '104', '105', '106', '107', '108'],
        [],
        ['109', '110', '111', '112', '113', '115', '116']
    ],
    // Этаж 1 (второй этаж)
    [
        ['202', '203', '204', '205', '206', '207', '208'],
        ['201', '217', '218'],
        ['209', '210', '211', '212', '213', '214', '215', '216'],
    ],
    // Этаж 2 (третий этаж)
    [
        ['302', '303', '304', '305', '306', '307'],
        ['301', '311'],
        [],
    ],
    // Этаж 3 (четвертый этаж)
    [
        ['405', '406', '407'],
        ['403', '404'],
        ['401']
    ]
];

// Словарь с координатами и описаниями
const roomDetails = {
    '101': { x: 0.2, y: 0.3, description: ""},
    '102': { x: 0.35, y: 0.3, description: ""},
    '103': { x: 0.45, y: 0.3, description: ""},
    '104': { x: 0.627, y: 0.3, description: ""},
    '105': { x: 0.785, y: 0.3, description: ""},
    '106': { x: 0.905, y: 0.3, description: ""},
    '107': { x: 0.7, y: 0.415, description: ""},
    '108': { x: 0.58, y: 0.415, description: ""},
    '109': { x: 0.35, y: 0.59, description: ""},
    '110': { x: 0.38, y: 0.653, description: ""},
    '111': { x: 0.36, y: 0.682, description: ""},
    '112': { x: 0.35, y: 0.735, description: "Учебный отдел"},
    '113': { x: 0.16, y: 0.72, description: "Приёмная"},
    '115': { x: 0.16, y: 0.668, description: "Зам. директора"},
    '116': { x: 0.16, y: 0.62, description: "Зам. директора"},

    '201': { x: 0.18, y: 0.3, description: ""},
    '202': { x: 0.33, y: 0.3, description: ""},
    '203': { x: 0.475, y: 0.3, description: ""},
    '204': { x: 0.627, y: 0.3, description: ""},
    '205': { x: 0.8, y: 0.3, description: ""},
    '206': { x: 0.923, y: 0.3, description: ""},
    '207': { x: 0.7, y: 0.415, description: ""},
    '208': { x: 0.58, y: 0.415, description: ""},
    '209': { x: 0.34, y: 0.55, description: ""},
    '210': { x: 0.34, y: 0.619, description: ""},
    '211': { x: 0.34, y: 0.71, description: ""},
    '212': { x: 0.34, y: 0.8, description: ""},
    '213': { x: 0.16, y: 0.765, description: ""},
    '214': { x: 0.16, y: 0.698, description: ""},
    '215': { x: 0.16, y: 0.61, description: ""},
    '216': { x: 0.16, y: 0.518, description: ""},
    '217': { x: 0.18, y: 0.47, description: ""},
    '218': { x: 0.18, y: 0.39, description: ""},

    '301': { x: 0.17, y: 0.3, description: ""},
    '302': { x: 0.325, y: 0.3, description: ""},
    '303': { x: 0.475, y: 0.3, description: ""},
    '304': { x: 0.622, y: 0.3, description: ""},
    '305': { x: 0.782, y: 0.3, description: ""},
    '306': { x: 0.91, y: 0.3, description: ""},
    '307': { x: 0.595, y: 0.415, description: ""},
    '311': { x: 0.17, y: 0.415, description: ""},

    '401': { x: 0.325, y: 0.475, description: ""},
    '403': { x: 0.17, y: 0.4, description: ""},
    '404': { x: 0.17, y: 0.3, description: ""},
    '405': { x: 0.335, y: 0.3, description: ""},
    '406': { x: 0.48, y: 0.3, description: ""},
    '407': { x: 0.7, y: 0.3, description: "Спортзал"},
    
};

// Названия крыльев
const wingNames = ['Левое крыло', 'Центр', 'Правое крыло'];

// Функция для поиска кабинета в структуре
function findRoomInStructure(roomNumber) {
    for (let floor = 0; floor < buildingStructure.length; floor++) {
        for (let wing = 0; wing < buildingStructure[floor].length; wing++) {
            if (buildingStructure[floor][wing].includes(roomNumber)) {
                return {
                    floor: floor + 1,
                    wing: wing,
                    wingName: wingNames[wing],
                    exists: true
                };
            }
        }
    }
    return { exists: false };
}