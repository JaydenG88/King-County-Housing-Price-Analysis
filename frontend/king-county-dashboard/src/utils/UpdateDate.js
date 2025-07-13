
export default async function UpdateDate() {
    try {
        const res = await fetch(
          `https://king-county-housing-price-analysis.onrender.com/api/date`
        );
        if (!res.ok) {
          throw new Error("Network response was not ok" + res.statusText);
        }
        const date = await res.json();
        if (!date || !date) {
            throw new Error("Invalid date format");
        }
        return date;

    } catch (error) {
        console.error("Error fetching update date:", error);
        return "Unknown";
    }

}