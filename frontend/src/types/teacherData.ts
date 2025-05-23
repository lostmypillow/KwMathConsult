export type teacherData = {
  role: "teacher";
  學號: string;
  姓名: string;
  大學: string;
  設備號碼: number;
};
export const defaultTeacher: teacherData = {
  role: "teacher",
  學號: "",
  姓名: "",
  大學: "",
  設備號碼: 0,
};
