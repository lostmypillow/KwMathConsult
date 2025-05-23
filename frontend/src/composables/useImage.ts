export const placeholderUrl = `http://${window.location.host}/dash/placeholder.png`;


export async function resolveImage(id: string): Promise<string> {
  const fallback = placeholderUrl
  const primary = `http://${import.meta.env.VITE_FASTAPI_URL}/picture/${id}`
  const secondary = `http://192.168.2.17:8002/picture/employee/${id}`

  return await tryImage(primary)
      || await tryImage(secondary)
      || fallback
}

function tryImage(url: string): Promise<string | null> {
  // Add a no-cache timestamp query param
  const noCacheUrl = `${url}?_=${Date.now()}`
  return new Promise(resolve => {
    const img = new Image()
    img.onload = () => resolve(noCacheUrl) // Return original URL, not timestamped one
    img.onerror = () => resolve(null)
    img.src = noCacheUrl
  })
}
