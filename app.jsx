import { Navigate, Route, Routes } from "react-router-dom";
import ClinicalTrials from "./pages/ClinicalTrials";
import LogicBuilder from "./pages/LogicBuilder";
import GenerateCohort from "./pages/GenerateCohort";
import PatientDetails from "./pages/PatientDetails";
import { ClinicalTrialsProvider } from "./context/ClinicalTrialsContext";
import CompleteTrialsAnalysis from "./pages/CompleteTrialsAnalysis";
import TrialsAnalysis from "./pages/TrialsAnalysis";
import NlpInput from "./pages/NlpInput";
import NLLogicBuilder from "./pages/NLLogicBuilder";
import NLGenerateCohort from "./pages/NLPGenerateCohort";
import NLPatientDetails from "./pages/NLPatientDetails";
import DecisionPage from "./pages/FirstPage";
import DecisionPage2 from "./pages/DecisionPage2";
import PatientMedicalDetails from "./pages/PatientMedicalDetails";
import LoginSignUp from "./pages/LoginSignUp";

import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./context/ProtectedRoute";
import Header from "./components/Header";

const App = () => {
  return (
    <AuthProvider>
      <ClinicalTrialsProvider>
      <Header />
        <Routes>
          <Route path="/auth-page" element={<LoginSignUp />} />
          <Route path="/" element={<LoginSignUp />} />

          <Route path="/nctid-input" element={
            <ProtectedRoute><DecisionPage2 /></ProtectedRoute>
          } />
          <Route path="/nlp-input" element={
            <ProtectedRoute><NlpInput /></ProtectedRoute>
          } />
          <Route path="/nl-logic-builder" element={
            <ProtectedRoute><NLLogicBuilder /></ProtectedRoute>
          } />
          <Route path="/generate-cohort" element={
            <ProtectedRoute><GenerateCohort /></ProtectedRoute>
          } />
          <Route path="/logic-builder" element={
            <ProtectedRoute><LogicBuilder /></ProtectedRoute>
          } />
          <Route path="/nl-generate-cohort" element={
            <ProtectedRoute><NLGenerateCohort /></ProtectedRoute>
          } />
          <Route path="/nl-patient-details" element={
            <ProtectedRoute><NLPatientDetails /></ProtectedRoute>
          } />
          <Route path="/patient-details" element={
            <ProtectedRoute><PatientDetails /></ProtectedRoute>
          } />
          <Route path="/patient-medical-details" element={
            <ProtectedRoute><PatientMedicalDetails /></ProtectedRoute>
          } />
          <Route path="/complete-analysis" element={
            <ProtectedRoute><CompleteTrialsAnalysis /></ProtectedRoute>
          } />
          <Route path="/trials" element={
            <ProtectedRoute><TrialsAnalysis /></ProtectedRoute>
          } />
          <Route path="/clinical-trials" element={
            <ProtectedRoute><ClinicalTrials /></ProtectedRoute>
          } />
        </Routes>
      </ClinicalTrialsProvider>
    </AuthProvider>
  );
};

export default App;
