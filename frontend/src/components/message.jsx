function Message({
    answer,
    sources,
    webSources
  }) {
  
    return (
  
      <div className="answer-card">
  
        <h3>
          🤖 AI Answer
        </h3>
  
  
        <div className="answer-text">
          {answer}
        </div>
  
  
        {/* PDF SOURCES */}
  
        {sources && sources.length > 0 && (
  
          <div className="sources">
  
            <h4>
              📄 Document Sources
            </h4>
  
            <div className="source-list">
  
              {sources.map((page) => (
  
                <span
                  className="source"
                  key={page}
                >
                  📄 Page {page}
                </span>
  
              ))}
  
            </div>
  
          </div>
  
        )}
  
  
        {/* WEB SOURCES */}
  
        {webSources && webSources.length > 0 && (
  
          <div className="web-sources">
  
            <h4>
              🌐 External Sources
            </h4>
  
  
            {webSources.map(
              (source, index) => (
  
                <a
                  key={index}
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="web-source"
                >
  
                  <strong>
                    {source.title}
                  </strong>
  
                  <span>
                    {source.url}
                  </span>
  
                </a>
  
              )
            )}
  
          </div>
  
        )}
  
      </div>
  
    );
  }
  
  
  export default Message;