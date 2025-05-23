import axios from "axios";
export function useAPI() {
  const uploadImage = async (canvas: any, employeeId: any) => {
    try {
      const blob: any = await new Promise((resolve) =>
        canvas.toBlob(resolve, "image/jpeg", 1)
      );
      const formData = new FormData();
      formData.append("file", blob, "cropped.jpg");

      await axios.post(
        `http://${import.meta.env.VITE_FASTAPI_URL}/picture/${employeeId}`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
    } catch (error) {
      throw new Error("Unknown error");
    }
  };
  const updateCollege = async (teacherData: any) => {
    try {
      await axios.post(
        `http://${import.meta.env.VITE_FASTAPI_URL}/update`,
        teacherData
      );
    } catch (error) {
      throw new Error("Unknown error");
    }
  };

  const getTeacherInfo = async (teacherId: any) => {
    try {
      const response = await axios.get(
        `http://${import.meta.env.VITE_FASTAPI_URL}/0/${teacherId}`
      );
      return response.data;
    } catch (error) {
      throw new Error("Unknown error");
    }
  };

  return { uploadImage, updateCollege, getTeacherInfo };
}
