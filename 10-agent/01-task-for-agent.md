# **E-commerce Analytics Streamlit App - Development Plan for Claude Code**

## **Project Overview**

Build a conversational data analytics tool using Streamlit that allows users to ask business questions about e-commerce data and receive rich, multi-modal insights combining text explanations, process diagrams, and interactive visualizations.

## **Pre-Development Setup**

### **Database Preparation (One-Time Activity)**

- Execute the provided `20-config/01-data_generator.py` script to create `database/my_ecommerce_db.duckdb`
- Verify database contains 10,000 e-commerce orders with complete schema
- Add the database file to the repository for direct use by the application
- Document the schema structure for LLM integration

### **Environment Configuration**

- **Local Development:** Use `.env` file with `OPENAI_API_KEY` and `DUCKDB_PATH` variables
- **Production Deployment:** Configure Streamlit secrets for API key and relative database path
- Set up proper environment variable handling for both scenarios

### Create & activate venv

- Create the venv once using the command:

  ```bash
  python3 -m venv venv
  ```

- For each session, activate the venv using:

  ```bash
  source venv/bin/activate
  ```

- Install dependencies using:
  ```bash
  pip install -r requirements.txt
  ```

---

## **Phase 1: Core Foundation (MVP)**

### **1.1 Project Structure Setup**

Create the following directory structure:

```
ecommerce_analytics/
├── main.py                    # Main Streamlit application
├── 30-database/
│   ├── connection.py          # DuckDB connection utilities
│   ├── schema.py             # Schema definitions for LLM context
│   └── my_ecommerce_db.duckdb # Pre-generated database
├── 40-llm/
│   ├── sql_agent.py          # LangChain SQL agent configuration
│   └── story_generator.py    # OpenAI story generation logic
├── 50-visualization/
│   ├── plotly_charts.py      # Data visualization components
│   └── mermaid_diagrams.py   # Process diagram utilities
├── .env                      # Environment variables (local)
├── requirements.txt          # Dependencies
└── README.md                 # Setup and usage instructions
```

### **1.2 Database Integration**

- Create connection utilities for DuckDB
- Define comprehensive schema information for LLM context including:
  - Complete column definitions with types
  - Sample data rows for reference
  - Business context for each field
  - Relationships and constraints
- Implement basic query execution functions
- Add connection testing and validation

### **1.3 Basic Streamlit Interface**

- Create two-tab layout: "Chat" and "View"
- **Chat Tab:**
  - Simple text input for questions
  - Static response: "Visit View tab for detailed analysis"
  - Clean, minimal interface focused on question collection
- **View Tab:**
  - Placeholder for rich content display
  - Loading state indicators
- Implement tab state management

### **1.4 LangChain SQL Agent Integration**

- Configure LangChain SQL agent with OpenAI
- Provide detailed schema context to the agent
- Implement basic query generation and execution
- Add fundamental error handling for invalid SQL
- Test with simple queries to verify functionality

### **1.5 Basic Error Handling**

- Wrap all external API calls in try-catch blocks
- Implement user-friendly error messages (no technical jargon)
- Add basic logging for debugging purposes
- Create fallback responses for common failure scenarios

---

## **Phase 2: Rich Content Generation**

### **2.1 Story Generation Framework**

- Design structured prompt templates for consistent LLM responses
- Implement response format with:
  - Executive summary (2-3 sentences)
  - Key insights (3-5 bullet points)
  - Visualization specifications
  - Explanatory context
- Add few-shot learning examples in prompts
- Implement JSON response parsing and validation

### **2.2 Visualization Strategy Implementation**

**Mermaid Diagrams - For Process/Conceptual Visualization:**

- Business processes (order workflows, customer journeys)
- Hierarchical relationships (category → subcategory → product)
- Decision trees and flowcharts
- Conceptual frameworks

**Plotly Charts - For Data Visualization:**

- Time series analysis (sales trends, seasonal patterns)
- Categorical comparisons (product categories, states)
- Distribution analysis (price ranges, order values)
- Correlation visualizations (price vs quantity relationships)

### **2.3 Content Integration**

- Implement View tab content generation pipeline
- Create dynamic content rendering based on query results
- Add proper spacing and formatting for multi-modal content
- Implement complete redraw functionality for new questions

---

## **Phase 3: Performance & Resilience**

### **3.1 Performance Optimization**

- **Query Result Limits:** Cap at 10,000 rows maximum
- **Timeout Management:** 30-second query timeout limit
- **Caching Strategy:**
  - Use `@st.cache_data` for SQL query results (5-10 minute TTL)
  - Cache LLM responses by question hash
  - Implement cache invalidation strategies
- **Memory Management:** Monitor DataFrame sizes before processing

### **3.2 Advanced Error Handling**

- **Retry Mechanisms:** 2-3 retry attempts for failed SQL generation
- **Query Validation:** Use sqlparse library for SQL syntax validation
- **API Resilience:** Implement exponential backoff for rate limits
- **Graceful Degradation:** Provide meaningful alternatives when systems fail

### **3.3 User Experience Enhancements**

- **Progressive Loading:** Multi-stage loading indicators
- **Input Validation:** Basic question format checking
- **Response Debouncing:** Wait 500ms after user input before processing
- **Operation Cancellation:** Allow users to stop long-running operations

---

## **Phase 4: Production Readiness**

### **4.1 Question Complexity Management**

- Implement question complexity scoring
- Provide user guidance for effective queries
- Create question templates and examples
- Add suggestion system for overly complex requests

### **4.2 Comprehensive Testing**

- Unit tests for database operations
- Integration tests for LLM interactions
- UI testing for Streamlit components
- Performance testing with various query types

### **4.3 Documentation & Deployment**

- Complete setup instructions
- Usage guidelines and best practices
- Troubleshooting guide
- Deployment documentation for Streamlit Cloud

---

## **Key Technical Decisions & Rationale**

### **Data Strategy**

- **Pre-built Database:** Eliminates runtime data generation complexity and ensures consistent testing environment
- **DuckDB Choice:** Optimized for analytical queries, better performance than SQLite for aggregations

### **Architecture Decisions**

- **Single-Turn Conversations:** Simplifies state management and reduces complexity for MVP
- **Separation of Concerns:** Clear distinction between quick chat interface and rich analysis view
- **Complete View Redraw:** Eliminates caching complexity and ensures fresh insights for each question

### **LLM Integration Approach**

- **Schema-Aware Agent:** Providing complete schema context improves query accuracy
- **Structured Responses:** JSON format ensures consistent parsing and display
- **Visualization Separation:** Clear roles for Mermaid (conceptual) vs Plotly (data) reduces confusion

---

## **Identified Risks & Mitigation Strategies**

### **High Priority Risks**

1. **Invalid SQL Generation:** Mitigated by validation, retry mechanisms, and comprehensive schema context
2. **API Rate Limits:** Handled through exponential backoff and circuit breaker patterns
3. **Performance Issues:** Addressed via result limits, timeouts, and strategic caching

### **Medium Priority Concerns**

1. **Question Complexity:** Managed through user guidance and complexity analysis
2. **Visualization Syntax Errors:** Reduced via prompt engineering and validation
3. **User Experience Flow:** Enhanced through progressive loading and clear feedback

### **Monitoring & Improvement**

- Log all failed queries for prompt improvement
- Track user question patterns for feature enhancement
- Monitor API usage and performance metrics
- Collect user feedback for iterative improvements

---

## **Success Criteria**

### **Functional Requirements**

- Users can ask natural language questions about e-commerce data
- System generates accurate SQL queries for business questions
- Rich stories combine text insights with relevant visualizations
- Application handles common error scenarios gracefully

### **Performance Requirements**

- Query responses within 30 seconds for typical questions
- Successful visualization generation for 90%+ of valid queries
- Stable operation under normal usage patterns

### **User Experience Goals**

- Intuitive interface requiring minimal learning curve
- Clear feedback during processing operations
- Meaningful error messages and recovery suggestions
- Engaging and informative data stories

This plan provides Claude Code with a comprehensive roadmap while maintaining flexibility for implementation decisions and iterative development approaches.
