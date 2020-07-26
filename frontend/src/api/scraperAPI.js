import api from './index'

export const fetchScrapers = () => api.get('api/scrapers')
export const createScraper = (data) => api.post('api/scrapers', data)
export const updateScraper = (data) => api.put('api/scrapers', data)
export const deleteScraper = (id) => api.delete('api/scrapers', {data: {id}} )
