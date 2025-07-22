/**
 * @name TestMind Security Analysis
 * @description Custom security queries for TestMind AI application (Python + React)
 * @kind problem
 * @id testmind/security-analysis
 * @problem.severity warning
 * @precision medium
 * @tags security
 *       external
 *       ai
 */

import python
import semmle.python.security
import semmle.python.web.security

/**
 * Detects potential prompt injection vulnerabilities in AI model inputs
 */
from AIInputValidation ai
where ai.hasUnvalidatedInput()
select ai, "Potential prompt injection vulnerability detected in AI model input"

/**
 * Detects potential command injection in system calls
 */
from CommandInjectionVulnerability cmd
where cmd.isVulnerable()
select cmd, "Potential command injection vulnerability detected"

/**
 * Detects potential path traversal vulnerabilities
 */
from PathTraversalVulnerability path
where path.isVulnerable()
select path, "Potential path traversal vulnerability detected"


/**
 * Detects potential data exposure in API responses
 */
from DataExposureVulnerability data
where data.isVulnerable()
select data, "Potential sensitive data exposure detected"

/**
 * Detects potential logging of sensitive information
 */
from SensitiveLoggingVulnerability log
where log.isVulnerable()
select log, "Potential sensitive information logging detected"

/**
 * Detects potential insecure deserialization
 */
from InsecureDeserializationVulnerability deser
where deser.isVulnerable()
select deser, "Potential insecure deserialization vulnerability detected"

/**
 * Detects potential XSS vulnerabilities in API responses
 */
from XSSVulnerability xss
where xss.isVulnerable()
select xss, "Potential XSS vulnerability detected in API response"

/**
 * Detects potential CSRF vulnerabilities
 */
from CSRFVulnerability csrf
where csrf.isVulnerable()
select csrf, "Potential CSRF vulnerability detected"

/**
 * Detects potential open redirect vulnerabilities
 */
from OpenRedirectVulnerability redirect
where redirect.isVulnerable()
select redirect, "Potential open redirect vulnerability detected"

/**
 * Detects potential information disclosure in error messages
 */
from InformationDisclosureVulnerability info
where info.isVulnerable()
select info, "Potential information disclosure in error messages"

/**
 * Detects potential insecure file operations
 */
from InsecureFileOperationVulnerability file
where file.isVulnerable()
select file, "Potential insecure file operation vulnerability detected"

/**
 * Detects potential insecure random number generation
 */
from InsecureRandomVulnerability random
where random.isVulnerable()
select random, "Potential insecure random number generation detected"

/**
 * Detects potential hardcoded credentials
 */
from HardcodedCredentialsVulnerability creds
where creds.isVulnerable()
select creds, "Potential hardcoded credentials detected"

/**
 * Detects potential weak cryptographic algorithms
 */
from WeakCryptographicAlgorithmVulnerability crypto
where crypto.isVulnerable()
select crypto, "Potential weak cryptographic algorithm detected" 