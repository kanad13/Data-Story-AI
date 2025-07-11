# **E-commerce Analytics Streamlit App - Development Plan for Claude Code**

## **Project Overview**

Build a conversational data analytics tool using Streamlit that allows users to ask business questions about e-commerce data and receive rich, multi-modal insights combining text explanations, process diagrams, and interactive visualizations.

## **Pre-Development Setup**

### **Database Preparation (One-Time Activity)**

- Execute the provided `20-config/01-data_generator.py` script to create `30-database/my_ecommerce_db.duckdb`
- Verify database contains 10,000 e-commerce orders with complete schema
- Add the database file to the repository for direct use by the application
- Document the schema structure for LLM integration

### **Environment Configuration**

- **Local Development:** Use `.env` file with required environment variables
- **Production Deployment:** Configure Streamlit secrets for API key and relative database path
- Set up proper environment variable handling for both scenarios

#### **Required Environment Variables**

```bash
# Required .env variables (create .env.example template)
OPENAI_API_KEY=your_api_key_here
DUCKDB_PATH=30-database/my_ecommerce_db.duckdb
STREAMLIT_THEME=light
LOG_LEVEL=INFO
CACHE_TTL=300  # 5 minutes
MAX_QUERY_ROWS=10000
QUERY_TIMEOUT=30
NUM_ORDERS=10000
NUM_CUSTOMERS=500
START_DATE=2023-01-01
END_DATE=2023-12-31
DB_OUTPUT_PATH=30-database/my_ecommerce_db.duckdb
```

### **Create & Activate Virtual Environment**

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

### **Database Schema Documentation Requirements**

Create comprehensive schema documentation including:

- Complete data dictionary with business definitions for each column
- Sample queries demonstrating table/column usage
- Data quality constraints and assumptions
- Relationship diagrams showing data flow
- Query performance considerations and indexing strategy
- Data validation rules and business logic constraints

---

## **Phase 1: Core Foundation (MVP)**

### **1.1 Project Structure Setup**

Create the following directory structure:

```
poly-base/
├── main.py                    # Main Streamlit application
├── 10-agent/                  # Agent instruction and workflow files
│   ├── 01-task-for-agent.md
│   ├── 02-instructions-for-agent.md
│   ├── 03-task-state-tracker.md
│   └── 04-response_guidelines.md
├── 20-config/                 # Configuration and data generation
│   └── 01-data_generator.py
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
├── tests/                    # Test files
│   ├── test_database.py     # Database connection tests
│   ├── test_llm.py          # LLM integration tests
│   └── test_ui.py           # UI component tests
├── .env                      # Environment variables (local)
├── .env.example             # Environment variable template
├── .gitignore              # Git ignore patterns
├── pytest.ini             # Test configuration
├── pyproject.toml          # Project metadata and tool configuration
├── requirements.txt        # Dependencies
└── README.md              # Setup and usage instructions
```

### **1.2 Database Integration**

- Create connection utilities for DuckDB with proper error handling
- Define comprehensive schema information for LLM context including:
  - Complete column definitions with types and business meanings
  - Sample data rows for reference and validation
  - Business context for each field with examples
  - Relationships and constraints between tables/fields
  - Performance optimization hints for common queries
- Implement basic query execution functions with timeout and result limits
- Add connection testing, validation, and health checks
- Create data validation functions for quality assurance

### **1.3 Basic Streamlit Interface**

- Create two-tab layout: "Chat" and "View"
- **Chat Tab:**
  - Simple text input for questions with validation
  - Static response: "Visit View tab for detailed analysis"
  - Clean, minimal interface focused on question collection
  - Input sanitization and basic validation
- **View Tab:**
  - Placeholder for rich content display
  - Loading state indicators with progress tracking
  - Error boundary components for graceful failure handling
- Implement tab state management and session persistence

### **1.4 LangChain SQL Agent Integration**

- Configure LangChain SQL agent with OpenAI API
- Provide detailed schema context to the agent with examples
- Implement basic query generation and execution with validation
- Add fundamental error handling for invalid SQL with retry mechanisms
- Test with simple queries to verify functionality
- Implement query result caching and performance monitoring

### **1.5 Basic Error Handling**

- Wrap all external API calls in try-catch blocks with specific error types
- Implement user-friendly error messages (no technical jargon)
- Add comprehensive logging for debugging with proper log levels
- Create fallback responses for common failure scenarios
- Implement circuit breaker patterns for external dependencies
- Add retry mechanisms with exponential backoff

---

## **Phase 2: Rich Content Generation**

### **2.1 Story Generation Framework**

- Design structured prompt templates for consistent LLM responses
- Implement response format with:
  - Executive summary (2-3 sentences)
  - Key insights (3-5 bullet points)
  - Visualization specifications with clear parameters
  - Explanatory context and business implications
- Add few-shot learning examples in prompts with diverse scenarios
- Implement JSON response parsing and validation with error recovery
- Create prompt optimization and A/B testing framework

### **2.2 Visualization Strategy Implementation**

**Mermaid Diagrams - For Process/Conceptual Visualization:**

- Business processes (order workflows, customer journeys)
- Hierarchical relationships (category → subcategory → product)
- Decision trees and flowcharts
- Conceptual frameworks and business logic flows

**Plotly Charts - For Data Visualization:**

- Time series analysis (sales trends, seasonal patterns)
- Categorical comparisons (product categories, states, payment methods)
- Distribution analysis (price ranges, order values, customer segments)
- Correlation visualizations (price vs quantity relationships)
- Geographic visualizations (sales by state/region)

### **2.3 Content Integration**

- Implement View tab content generation pipeline with proper sequencing
- Create dynamic content rendering based on query results
- Add proper spacing and formatting for multi-modal content
- Implement complete redraw functionality for new questions
- Add content validation and quality checks
- Create responsive design for different screen sizes

---

## **Phase 3: Performance & Resilience**

### **3.1 Performance Optimization**

- **Query Result Limits:** Cap at 10,000 rows maximum with configurable limits
- **Timeout Management:** 30-second query timeout with graceful handling
- **Caching Strategy:**
  - Use `@st.cache_data` for SQL query results (5-10 minute TTL)
  - Cache LLM responses by question hash with TTL management
  - Implement cache invalidation strategies and cache warming
  - Monitor cache hit rates and performance impact
- **Memory Management:** Monitor DataFrame sizes before processing with limits
- **Database Connection Pooling:** Efficient connection management
- **Query Optimization:** Analyze and optimize slow queries

### **3.2 Advanced Error Handling**

- **Retry Mechanisms:** 2-3 retry attempts for failed SQL generation with backoff
- **Query Validation:** Use sqlparse library for SQL syntax validation
- **API Resilience:** Implement exponential backoff for rate limits
- **Graceful Degradation:** Provide meaningful alternatives when systems fail
- **Circuit Breaker Patterns:** Prevent cascade failures in external dependencies
- **Health Checks:** Monitor system components and dependencies
- **Error Analytics:** Track error patterns for system improvement

### **3.3 User Experience Enhancements**

- **Progressive Loading:** Multi-stage loading indicators with meaningful messages
- **Input Validation:** Basic question format checking and sanitization
- **Response Debouncing:** Wait 500ms after user input before processing
- **Operation Cancellation:** Allow users to stop long-running operations
- **Session Management:** Maintain user context and preferences
- **Accessibility:** Ensure WCAG compliance for UI components
- **Mobile Responsiveness:** Optimize for mobile and tablet interfaces

---

## **Phase 4: Production Readiness**

### **4.1 Question Complexity Management**

- Implement question complexity scoring algorithm
- Provide user guidance for effective queries with examples
- Create question templates and examples for different use cases
- Add suggestion system for overly complex requests
- Implement query decomposition for complex multi-part questions
- Create query history and favorites functionality

### **4.2 Comprehensive Testing**

#### **Testing Implementation Details**

- **Unit Tests:** pytest for database connections, query validation, data processing
- **Integration Tests:** LangChain agent behavior, OpenAI API integration, end-to-end workflows
- **End-to-End Tests:** Streamlit UI automation using selenium or playwright
- **Performance Tests:** Query response times, memory usage profiling, load testing
- **Error Scenario Tests:** Invalid SQL, API failures, timeout handling, edge cases
- **Security Tests:** Input validation, injection attacks, authentication bypass
- **Accessibility Tests:** Screen reader compatibility, keyboard navigation
- **Cross-browser Tests:** Chrome, Firefox, Safari compatibility

#### **Test Coverage Requirements**

- Minimum 80% code coverage for critical components
- 100% coverage for database operations and security functions
- Performance benchmarks for all major user flows
- Automated regression testing for each deployment

### **4.3 Documentation & Deployment**

- Complete setup instructions with troubleshooting guide
- Usage guidelines and best practices with examples
- API documentation for all components
- Deployment documentation for Streamlit Cloud and other platforms
- Security configuration guide
- Performance tuning recommendations
- Backup and disaster recovery procedures

---

## **Security Considerations**

### **Input Security**

- Sanitize all user inputs to prevent injection attacks
- Validate query parameters and SQL generation
- Implement rate limiting for API calls and user requests
- Add CSRF protection for form submissions

### **API Security**

- Secure API key storage and rotation procedures
- Implement proper authentication and authorization
- Monitor API usage and detect anomalous patterns
- Add request signing and validation

### **Data Security**

- Encrypt sensitive data at rest and in transit
- Implement proper access controls and audit logging
- Regular security scans and vulnerability assessments
- Data privacy compliance (GDPR, CCPA considerations)

---

## **Key Technical Decisions & Rationale**

### **Data Strategy**

- **Pre-built Database:** Eliminates runtime data generation complexity and ensures consistent testing environment
- **DuckDB Choice:** Optimized for analytical queries, better performance than SQLite for aggregations
- **Schema Documentation:** Comprehensive context improves LLM query accuracy and reduces errors

### **Architecture Decisions**

- **Single-Turn Conversations:** Simplifies state management and reduces complexity for MVP
- **Separation of Concerns:** Clear distinction between quick chat interface and rich analysis view
- **Complete View Redraw:** Eliminates caching complexity and ensures fresh insights for each question
- **Modular Design:** Separate components for easy testing and maintenance

### **LLM Integration Approach**

- **Schema-Aware Agent:** Providing complete schema context improves query accuracy
- **Structured Responses:** JSON format ensures consistent parsing and display
- **Visualization Separation:** Clear roles for Mermaid (conceptual) vs Plotly (data) reduces confusion
- **Error Recovery:** Multiple fallback strategies for robust operation

---

## **Identified Risks & Mitigation Strategies**

### **High Priority Risks**

1. **Invalid SQL Generation:** Mitigated by validation, retry mechanisms, comprehensive schema context, and query testing
2. **API Rate Limits:** Handled through exponential backoff, circuit breaker patterns, and usage monitoring
3. **Performance Issues:** Addressed via result limits, timeouts, strategic caching, and performance monitoring
4. **Security Vulnerabilities:** Prevented through input validation, secure coding practices, and regular security audits

### **Medium Priority Concerns**

1. **Question Complexity:** Managed through user guidance, complexity analysis, and query decomposition
2. **Visualization Syntax Errors:** Reduced via prompt engineering, validation, and error recovery
3. **User Experience Flow:** Enhanced through progressive loading, clear feedback, and accessibility features
4. **Data Quality Issues:** Addressed through validation, constraints, and quality monitoring

### **Monitoring & Improvement**

- Log all failed queries for prompt improvement and pattern analysis
- Track user question patterns for feature enhancement and optimization
- Monitor API usage and performance metrics with alerting
- Collect user feedback for iterative improvements and feature requests
- Implement A/B testing for prompt optimization and UI improvements

---

## **Success Criteria**

### **Functional Requirements**

- Users can ask natural language questions about e-commerce data with 95% success rate
- System generates accurate SQL queries for business questions with proper error handling
- Rich stories combine text insights with relevant visualizations consistently
- Application handles common error scenarios gracefully without crashes
- Response time under 30 seconds for 90% of queries

### **Performance Requirements**

- Query responses within 30 seconds for typical questions
- Successful visualization generation for 90%+ of valid queries
- Stable operation under normal usage patterns (50+ concurrent users)
- Memory usage under 1GB for typical workloads
- 99.5% uptime during business hours

### **User Experience Goals**

- Intuitive interface requiring minimal learning curve (< 5 minutes to first success)
- Clear feedback during processing operations with progress indicators
- Meaningful error messages and recovery suggestions
- Engaging and informative data stories that provide business value
- Accessible design meeting WCAG 2.1 AA standards

### **Security & Compliance Goals**

- No security vulnerabilities in production deployment
- Proper data handling and privacy protection
- Audit trail for all user actions and system operations
- Compliance with relevant data protection regulations

This plan provides Claude Code with a comprehensive roadmap while maintaining flexibility for implementation decisions and iterative development approaches. The enhanced specifications should significantly improve the robustness and production-readiness of the final application.
