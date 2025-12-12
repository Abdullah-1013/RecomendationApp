const BASE_URL = "http://192.168.0.101:5001"; // Autofill backend IP

export const autofillProduct = async (table, name) => {
  try {
    const res = await fetch(`${BASE_URL}/autofill/${table}?name=${encodeURIComponent(name)}`);
    if (!res.ok) throw new Error("Failed to fetch autofill");
    return await res.json();
  } catch (err) {
    console.log(err);
    return null;
  }
};
