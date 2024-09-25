import React from 'react';

function LogsViewer() {
  return (
    <div>
      <iframe
        src="http://localhost:5601/app/kibana"
        title="Kibana Logs Viewer"
        width="100%"
        height="800px"
        style={{ border: 'none' }}
      ></iframe>
    </div>
  );
}

export default LogsViewer;
