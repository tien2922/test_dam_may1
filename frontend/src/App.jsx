import React, { useEffect, useState } from 'react'

const API = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080'

async function api(path, opts={}){
  const res = await fetch(API + path, { headers: { 'Content-Type':'application/json' }, ...opts })
  if(!res.ok) throw new Error(await res.text()); return res.json()
}

function Section({title, children}){
  return <div style={{border:'1px solid #ddd', borderRadius:12, padding:16, margin:'16px 0'}}>
    <h2 style={{marginTop:0}}>{title}</h2>
    {children}
  </div>
}

export default function App(){
  const [health,setHealth] = useState('unknown')
  const [tab,setTab] = useState('products')

  useEffect(()=>{ api('/health').then(d=>setHealth(JSON.stringify(d))).catch(()=>setHealth('error')) },[])

  return (
    <div style={{maxWidth:1100, margin:'32px auto', fontFamily:'system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif', padding:'0 16px'}}>
      <h1>BDU Inventory Management</h1>
      <p style={{marginTop:0}}>React (Vite) → FastAPI → MySQL</p>
      <div style={{display:'flex', gap:8}}>
        {['products','suppliers','stock'].map(k=>
          <button key={k} onClick={()=>setTab(k)} style={{padding:'8px 12px', borderRadius:8, border:'1px solid #ccc', background: tab===k?'#eef':'#f7f7f7'}}>{k.toUpperCase()}</button>
        )}
      </div>

      <Section title="Health">{health}</Section>

      {tab==='products' && <Products/>}
      {tab==='suppliers' && <Suppliers/>}
      {tab==='stock' && <StockMoves/>}
    </div>
  )
}

function Products(){
  const empty = { sku:'', name:'', unit_price:0 }
  const [form, setForm] = useState(empty)
  const [rows, setRows] = useState([])

  const load = async()=> setRows(await api('/api/products'))
  useEffect(()=>{ load() },[])

  async function save(){
    if(!form.sku || !form.name) return
    await api('/api/products', { method:'POST', body: JSON.stringify({...form, unit_price:Number(form.unit_price)||0}) })
    setForm(empty); await load()
  }
  async function del(id){ await api('/api/products/'+id, { method:'DELETE' }); await load() }
  async function edit(r){
    const name = prompt('Name:', r.name); if(!name) return
    const unit = prompt('Unit price:', r.unit_price); if(unit==null) return
    await api('/api/products/'+r.id, { method:'PUT', body: JSON.stringify({ sku:r.sku, name, unit_price:Number(unit)||0 }) })
    await load()
  }

  return <Section title="Products">
    <div style={{display:'grid', gap:8, gridTemplateColumns:'repeat(4, 1fr)'}}>
      <input placeholder="SKU" value={form.sku} onChange={e=>setForm({...form, sku:e.target.value})}/>
      <input placeholder="Name" value={form.name} onChange={e=>setForm({...form, name:e.target.value})}/>
      <input type="number" step="0.01" placeholder="Unit Price" value={form.unit_price} onChange={e=>setForm({...form, unit_price:e.target.value})}/>
      <button onClick={save}>Add</button>
    </div>
    <table style={{width:'100%', marginTop:12, borderCollapse:'collapse'}}>
      <thead><tr><th>ID</th><th>SKU</th><th>Name</th><th>Unit Price</th><th>Stock</th><th>Actions</th></tr></thead>
      <tbody>
        {rows.map(r=>(
          <tr key={r.id}>
            <td>{r.id}</td><td>{r.sku}</td><td>{r.name}</td>
            <td>{Number(r.unit_price).toFixed(2)}</td><td>{r.stock}</td>
            <td>
              <button onClick={()=>edit(r)}>Edit</button>
              <button style={{marginLeft:6}} onClick={()=>del(r.id)}>Delete</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </Section>
}

function Suppliers(){
  const empty = { name:'', email:'', phone:'' }
  const [form, setForm] = useState(empty)
  const [rows, setRows] = useState([])
  const load = async()=> setRows(await api('/api/suppliers'))
  useEffect(()=>{ load() },[])

  async function save(){
    if(!form.name) return
    await api('/api/suppliers', { method:'POST', body: JSON.stringify(form) })
    setForm(empty); await load()
  }
  async function del(id){ await api('/api/suppliers/'+id, { method:'DELETE' }); await load() }
  async function edit(r){
    const name = prompt('Name:', r.name); if(!name) return
    const email = prompt('Email:', r.email||''); if(email==null) return
    const phone = prompt('Phone:', r.phone||''); if(phone==null) return
    await api('/api/suppliers/'+r.id, { method:'PUT', body: JSON.stringify({ name, email, phone }) })
    await load()
  }

  return <Section title="Suppliers">
    <div style={{display:'grid', gap:8, gridTemplateColumns:'repeat(4, 1fr)'}}>
      <input placeholder="Name" value={form.name} onChange={e=>setForm({...form, name:e.target.value})}/>
      <input placeholder="Email" value={form.email} onChange={e=>setForm({...form, email:e.target.value})}/>
      <input placeholder="Phone" value={form.phone} onChange={e=>setForm({...form, phone:e.target.value})}/>
      <button onClick={save}>Add</button>
    </div>
    <table style={{width:'100%', marginTop:12, borderCollapse:'collapse'}}>
      <thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Actions</th></tr></thead>
      <tbody>
        {rows.map(r=>(
          <tr key={r.id}>
            <td>{r.id}</td><td>{r.name}</td><td>{r.email||''}</td><td>{r.phone||''}</td>
            <td>
              <button onClick={()=>edit(r)}>Edit</button>
              <button style={{marginLeft:6}} onClick={()=>del(r.id)}>Delete</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </Section>
}

function StockMoves(){
  const empty = { product_id:'', quantity:1, move_type:'IN', note:'' }
  const [form, setForm] = useState(empty)
  const [moves, setMoves] = useState([])
  const [products, setProducts] = useState([])

  const load = async()=> {
    setMoves(await api('/api/stock_moves'))
    setProducts(await api('/api/products'))
  }
  useEffect(()=>{ load() },[])

  async function apply(){
    const payload = {...form, product_id:Number(form.product_id), quantity:Number(form.quantity)}
    await api('/api/stock_moves', { method:'POST', body: JSON.stringify(payload) })
    setForm(empty); await load()
  }

  return <Section title="Stock Movements">
    <div style={{display:'grid', gap:8, gridTemplateColumns:'160px 1fr 1fr 1fr'}}>
      <select value={form.product_id} onChange={e=>setForm({...form, product_id:e.target.value})}>
        <option value="">-- Select Product --</option>
        {products.map(p=>(<option key={p.id} value={p.id}>{p.sku} - {p.name} (stock {p.stock})</option>))}
      </select>
      <select value={form.move_type} onChange={e=>setForm({...form, move_type:e.target.value})}>
        <option value="IN">IN</option>
        <option value="OUT">OUT</option>
      </select>
      <input type="number" min="1" value={form.quantity} onChange={e=>setForm({...form, quantity:e.target.value})}/>
      <input placeholder="Note" value={form.note} onChange={e=>setForm({...form, note:e.target.value})}/>
    </div>
    <div style={{marginTop:8}}><button onClick={apply}>Apply Move</button></div>

    <table style={{width:'100%', marginTop:12, borderCollapse:'collapse'}}>
      <thead><tr><th>ID</th><th>Product</th><th>Type</th><th>Qty</th><th>Note</th><th>Time</th></tr></thead>
      <tbody>
        {moves.map(m=>{
          const p = products.find(x=>x.id===m.product_id)
          return (<tr key={m.id}>
            <td>{m.id}</td>
            <td>{p ? `${p.sku} - ${p.name}` : m.product_id}</td>
            <td>{m.move_type}</td>
            <td>{m.quantity}</td>
            <td>{m.note||''}</td>
            <td>{m.created_at||''}</td>
          </tr>)
        })}
      </tbody>
    </table>
  </Section>
}
