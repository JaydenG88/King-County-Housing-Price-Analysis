import AveragesChart from "./components/AveragesChart"
export default function HomePage() {
  return (
    <main style={{ padding: '2rem' }}>
      <h1>King County Housing Dashboard</h1>
      <AveragesChart metric="price" type="mean" />
    </main>
  )
}