import AveragesChart from "./components/AveragesChart"
import OverTimeChart from "./components/OverTimeChart"
export default function HomePage() {
  return (
    <main style={{ padding: '2rem' }}>
      <h1>King County Housing Dashboard</h1>
      <OverTimeChart metric="price" type="mean" region="King County" />
    </main>
  )
}