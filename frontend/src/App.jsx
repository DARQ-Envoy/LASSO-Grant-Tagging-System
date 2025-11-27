import { useState, useEffect } from 'react';

function App() {
  const [activeTab, setActiveTab] = useState('view');
  const [grants, setGrants] = useState([]);
  const [selectedTags, setSelectedTags] = useState([]);
  const [allTags, setAllTags] = useState([]);
  
  const [grantName, setGrantName] = useState('');
  const [grantDescription, setGrantDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const fetchGrants = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/grants');
      const data = await response.json();
      setGrants(data.grants || []);
      
      const tags = new Set();
      data.grants?.forEach(grant => {
        grant.tags?.forEach(tag => tags.add(tag));
      });
      setAllTags(Array.from(tags).sort());
    } catch (error) {
      console.error('Error fetching grants:', error);
    }
  };

  useEffect(() => {
    fetchGrants();
  }, []);

  const handleAddGrant = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const response = await fetch('http://localhost:5000/api/grants', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          grant: {
            grant_name: grantName,
            grant_description: grantDescription
          }
        })
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to add grant');
      }
      
      setMessage('Grant added successfully!');
      setGrantName('');
      setGrantDescription('');
      await fetchGrants();
    } catch (error) {
      setMessage('Error adding grant: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const toggleTagFilter = (tag) => {
    setSelectedTags(prev => 
      prev.includes(tag) 
        ? prev.filter(t => t !== tag)
        : [...prev, tag]
    );
  };

  const filteredGrants = selectedTags.length === 0 
    ? grants 
    : grants.filter(grant => 
        grant.tags?.some(tag => selectedTags.includes(tag))
      );

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Grant Tagging System</h1>
          <p className="text-gray-600 mt-1">Add and manage grant opportunities</p>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 mt-6">
        <div className="border-b border-gray-200">
          <nav className="flex gap-4">
            <button
              onClick={() => setActiveTab('view')}
              className={`px-4 py-2 font-medium border-b-2 transition-colors ${
                activeTab === 'view'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              Grants ({grants.length})
            </button>
            <button
              onClick={() => setActiveTab('add')}
              className={`px-4 py-2 font-medium border-b-2 transition-colors ${
                activeTab === 'add'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              Add Grants
            </button>
          </nav>
        </div>
      </div>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {activeTab === 'add' ? (
          <div className="max-w-2xl mx-auto">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-4">Add Single Grant</h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Grant Name
                  </label>
                  <input
                    type="text"
                    value={grantName}
                    onChange={(e) => setGrantName(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Enter grant name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Grant Description
                  </label>
                  <textarea
                    value={grantDescription}
                    onChange={(e) => setGrantDescription(e.target.value)}
                    rows={6}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Enter grant description"
                  />
                </div>
                <button
                  onClick={handleAddGrant}
                  disabled={loading || !grantName.trim() || !grantDescription.trim()}
                  className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
                >
                  {loading ? 'Adding...' : 'Add Grant'}
                </button>
              </div>
            </div>

            {message && (
              <div className="mt-4">
                <div className={`p-4 rounded-md ${
                  message.includes('Error') 
                    ? 'bg-red-50 text-red-800 border border-red-200' 
                    : 'bg-green-50 text-green-800 border border-green-200'
                }`}>
                  {message}
                </div>
              </div>
            )}
          </div>
        ) : (
          <div>
            {allTags.length > 0 && (
              <div className="bg-white rounded-lg shadow p-6 mb-6">
                <h2 className="text-xl font-semibold mb-4">Filter by Tags</h2>
                <div className="flex flex-wrap gap-2">
                  {allTags.map(tag => (
                    <button
                      key={tag}
                      onClick={() => toggleTagFilter(tag)}
                      className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                        selectedTags.includes(tag)
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      }`}
                    >
                      {tag}
                    </button>
                  ))}
                </div>
                {selectedTags.length > 0 && (
                  <button
                    onClick={() => setSelectedTags([])}
                    className="mt-3 text-sm text-blue-600 hover:text-blue-800"
                  >
                    Clear filters
                  </button>
                )}
              </div>
            )}

            <div className="space-y-4">
              {filteredGrants.length === 0 ? (
                <div className="bg-white rounded-lg shadow p-8 text-center text-gray-500">
                  {grants.length === 0 
                    ? 'No grants added yet. Go to "Add Grants" tab to get started.'
                    : 'No grants match the selected filters.'}
                </div>
              ) : (
                filteredGrants.map((grant, index) => (
                  <div key={index} className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      {grant.grant_name}
                    </h3>
                    <p className="text-gray-700 mb-4">
                      {grant.grant_description}
                    </p>
                    {grant.tags && grant.tags.length > 0 && (
                      <div className="flex flex-wrap gap-2">
                        {grant.tags.map((tag, tagIndex) => (
                          <span
                            key={tagIndex}
                            className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;