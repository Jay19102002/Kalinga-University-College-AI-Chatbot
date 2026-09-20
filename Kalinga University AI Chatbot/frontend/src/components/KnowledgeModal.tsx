import React, { useState, useEffect } from 'react';
import {
  X, BookOpen, Award, Briefcase, GraduationCap, DollarSign,
  Search, FileText, Bookmark, Lightbulb, Calendar, Globe,
  Database, ChevronLeft, ChevronRight, ExternalLink, RefreshCw
} from 'lucide-react';
import {
  getKnowledgeData, getDatabaseStats, searchDatabase,
  getResearchPapers, getBooks, getNewsEvents, getWebPages, getDataTables
} from '../services/api';
import { FALLBACK_FEES } from '../data/feesData';

interface KnowledgeModalProps {
  isOpen: boolean;
  onClose: () => void;
}

type TabType =
  | 'search'
  | 'fees'
  | 'faqs'
  | 'career_paths'
  | 'research'
  | 'books'
  | 'patents'
  | 'internships'
  | 'news'
  | 'directory'
  | 'placements_scholarships';

export const KnowledgeModal: React.FC<KnowledgeModalProps> = ({ isOpen, onClose }) => {
  const [activeTab, setActiveTab] = useState<TabType>('fees');
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);

  // Global search state
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [searchFilter, setSearchFilter] = useState<string>('');

  // Tab specific data states
  const [feesData, setFeesData] = useState<any[]>(FALLBACK_FEES);
  const [feesLevelFilter, setFeesLevelFilter] = useState<string>('ALL');
  const [feesSearch, setFeesSearch] = useState<string>('');

  const [faqsData, setFaqsData] = useState<any[]>([]);
  const [faqsSearch, setFaqsSearch] = useState<string>('');

  const [careerPathsData, setCareerPathsData] = useState<any[]>([]);
  const [careerSearch, setCareerSearch] = useState<string>('');

  const [papersData, setPapersData] = useState<any>(null);
  const [papersPage, setPapersPage] = useState<number>(1);
  const [papersSearch, setPapersSearch] = useState<string>('');

  const [booksData, setBooksData] = useState<any>(null);
  const [booksPage, setBooksPage] = useState<number>(1);
  const [booksSearch, setBooksSearch] = useState<string>('');

  const [patentsData, setPatentsData] = useState<any[]>([]);
  const [patentsSearch, setPatentsSearch] = useState<string>('');

  const [internshipsSubTab, setInternshipsSubTab] = useState<'internships' | 'mous'>('internships');
  const [internshipsData, setInternshipsData] = useState<any[]>([]);
  const [mousData, setMousData] = useState<any[]>([]);
  const [internshipsSearch, setInternshipsSearch] = useState<string>('');

  const [newsData, setNewsData] = useState<any[]>([]);
  const [newsSearch, setNewsSearch] = useState<string>('');

  const [directorySubTab, setDirectorySubTab] = useState<'pages' | 'tables'>('pages');
  const [pagesData, setPagesData] = useState<any[]>([]);
  const [tablesData, setTablesData] = useState<any[]>([]);
  const [directorySearch, setDirectorySearch] = useState<string>('');

  const [placementsData, setPlacementsData] = useState<any>(null);
  const [scholarshipsData, setScholarshipsData] = useState<any>(null);

  // Fetch initial stats and active tab data on open
  useEffect(() => {
    if (isOpen) {
      loadStats();
      loadTabData(activeTab);
    }
  }, [isOpen, activeTab]);

  const loadStats = async () => {
    try {
      const s = await getDatabaseStats();
      setStats(s);
    } catch (e) {
      console.warn('Failed to load DB stats', e);
    }
  };

  const loadTabData = async (tab: TabType) => {
    setLoading(true);
    try {
      if (tab === 'fees') {
        try {
          const res = await getKnowledgeData('fees');
          const records = res?.fee_records || res?.data?.fee_records || res?.data || (Array.isArray(res) ? res : []);
          if (Array.isArray(records) && records.length > 0) {
            setFeesData(records);
          }
        } catch (err) {
          console.warn('API fetch for fees failed, keeping fallback data:', err);
        }
      } else if (tab === 'faqs' && faqsData.length === 0) {
        const res = await getKnowledgeData('faqs');
        setFaqsData(res.data?.faqs || res.matches || []);
      } else if (tab === 'career_paths' && careerPathsData.length === 0) {
        const res = await getKnowledgeData('career_paths');
        setCareerPathsData(res.data?.career_paths || res.matches || []);
      } else if (tab === 'research') {
        const res = await getResearchPapers(papersPage, 20, papersSearch || undefined);
        setPapersData(res);
      } else if (tab === 'books') {
        const res = await getBooks(booksPage, 20, booksSearch || undefined);
        setBooksData(res);
      } else if (tab === 'patents' && patentsData.length === 0) {
        const res = await getKnowledgeData('patents');
        setPatentsData(res.patents || res.data?.patents || []);
      } else if (tab === 'internships') {
        if (internshipsData.length === 0) {
          const res = await getKnowledgeData('internships');
          setInternshipsData(res.records || res.data?.records || []);
        }
        if (mousData.length === 0) {
          const resMous = await getKnowledgeData('mous');
          setMousData(resMous.mous || resMous.data?.mous || []);
        }
      } else if (tab === 'news' && newsData.length === 0) {
        const res = await getNewsEvents();
        setNewsData(res.events || []);
      } else if (tab === 'directory') {
        if (pagesData.length === 0) {
          const resPages = await getWebPages();
          setPagesData(resPages.pages || []);
        }
        if (tablesData.length === 0) {
          const resTables = await getDataTables();
          setTablesData(resTables.tables || []);
        }
      } else if (tab === 'placements_scholarships') {
        if (!placementsData) {
          const p = await getKnowledgeData('placements');
          setPlacementsData(p);
        }
        if (!scholarshipsData) {
          const s = await getKnowledgeData('scholarships');
          setScholarshipsData(s);
        }
      }
    } catch (err) {
      console.error('Error fetching tab data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleGlobalSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    setLoading(true);
    try {
      const res = await searchDatabase(searchQuery.trim(), searchFilter || undefined, 30);
      setSearchResults(res.results || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handlePapersSearchSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setPapersPage(1);
    setLoading(true);
    try {
      const res = await getResearchPapers(1, 20, papersSearch);
      setPapersData(res);
    } finally {
      setLoading(false);
    }
  };

  const handleBooksSearchSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setBooksPage(1);
    setLoading(true);
    try {
      const res = await getBooks(1, 20, booksSearch);
      setBooksData(res);
    } finally {
      setLoading(false);
    }
  };

  const changePapersPage = async (newPage: number) => {
    if (newPage < 1 || (papersData && newPage > papersData.total_pages)) return;
    setPapersPage(newPage);
    setLoading(true);
    try {
      const res = await getResearchPapers(newPage, 20, papersSearch || undefined);
      setPapersData(res);
    } finally {
      setLoading(false);
    }
  };

  const changeBooksPage = async (newPage: number) => {
    if (newPage < 1 || (booksData && newPage > booksData.total_pages)) return;
    setBooksPage(newPage);
    setLoading(true);
    try {
      const res = await getBooks(newPage, 20, booksSearch || undefined);
      setBooksData(res);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  // Filtered lists
  const filteredFees = feesData.filter((r: any) => {
    const levelUpper = (r.level || '').toUpperCase();
    const progLower = (r.program || '').toLowerCase();
    const shortLower = (r.short_name || '').toLowerCase();
    const deptLower = (r.department || '').toLowerCase();
    const durLower = (r.duration || '').toLowerCase();

    let matchesLevel = false;
    if (feesLevelFilter === 'ALL') {
      matchesLevel = true;
    } else if (feesLevelFilter === 'UG') {
      matchesLevel = levelUpper === 'UG' || durLower.includes('ug') || progLower.startsWith('bachelor') || shortLower.startsWith('b.');
    } else if (feesLevelFilter === 'PG') {
      matchesLevel = levelUpper === 'PG' || levelUpper === 'PG DIPLOMA' || durLower.includes('pg') || progLower.startsWith('master') || shortLower.startsWith('m.') || shortLower.includes('mba') || shortLower.includes('mca') || shortLower.includes('llm');
    } else if (feesLevelFilter === 'Diploma') {
      matchesLevel = levelUpper === 'DIPLOMA' || levelUpper === 'PG DIPLOMA' || progLower.includes('diploma') || shortLower.includes('diploma');
    }

    const searchLower = feesSearch.trim().toLowerCase();
    const matchesSearch =
      !searchLower ||
      progLower.includes(searchLower) ||
      shortLower.includes(searchLower) ||
      deptLower.includes(searchLower);

    return matchesLevel && matchesSearch;
  });

  const filteredFaqs = faqsData.filter((f: any) =>
    !faqsSearch || f.question.toLowerCase().includes(faqsSearch.toLowerCase()) || f.course.toLowerCase().includes(faqsSearch.toLowerCase()) || f.answer.toLowerCase().includes(faqsSearch.toLowerCase())
  );

  const filteredCareers = careerPathsData.filter((c: any) =>
    !careerSearch || c.career_path.toLowerCase().includes(careerSearch.toLowerCase()) || c.course.toLowerCase().includes(careerSearch.toLowerCase()) || c.description.toLowerCase().includes(careerSearch.toLowerCase())
  );

  const filteredPatents = patentsData.filter((p: any) =>
    !patentsSearch || p.topic.toLowerCase().includes(patentsSearch.toLowerCase()) || (p.inventor && p.inventor.toLowerCase().includes(patentsSearch.toLowerCase()))
  );

  const filteredInternships = internshipsData.filter((i: any) =>
    !internshipsSearch || (i.company && i.company.toLowerCase().includes(internshipsSearch.toLowerCase())) || (i.student && i.student.toLowerCase().includes(internshipsSearch.toLowerCase())) || (i.course && i.course.toLowerCase().includes(internshipsSearch.toLowerCase()))
  );

  const filteredMous = mousData.filter((m: any) =>
    !internshipsSearch || (m.partner && m.partner.toLowerCase().includes(internshipsSearch.toLowerCase())) || (m.faculty && m.faculty.toLowerCase().includes(internshipsSearch.toLowerCase()))
  );

  const filteredNews = newsData.filter((n: any) =>
    !newsSearch || n.heading.toLowerCase().includes(newsSearch.toLowerCase()) || n.summary.toLowerCase().includes(newsSearch.toLowerCase()) || (n.category && n.category.toLowerCase().includes(newsSearch.toLowerCase()))
  );

  const filteredPages = pagesData.filter((p: any) =>
    !directorySearch || p.title.toLowerCase().includes(directorySearch.toLowerCase()) || p.slug.toLowerCase().includes(directorySearch.toLowerCase()) || p.meta_description.toLowerCase().includes(directorySearch.toLowerCase())
  );

  const filteredTables = tablesData.filter((t: any) =>
    !directorySearch || t.title.toLowerCase().includes(directorySearch.toLowerCase()) || (t.category && t.category.toLowerCase().includes(directorySearch.toLowerCase())) || (t.headers && t.headers.toLowerCase().includes(directorySearch.toLowerCase()))
  );

  const tabs = [
    { id: 'search', label: 'Global FTS Search', icon: Search, count: stats?.fts_indexed_documents || 10967 },
    { id: 'fees', label: 'Programs & Fees', icon: DollarSign, count: stats?.courses || feesData.length || 69 },
    { id: 'faqs', label: 'Course FAQs', icon: BookOpen, count: stats?.course_faqs || 355 },
    { id: 'career_paths', label: 'Career Paths', icon: GraduationCap, count: stats?.career_paths || 621 },
    { id: 'research', label: 'Research Papers', icon: FileText, count: stats?.research_papers || 4866 },
    { id: 'books', label: 'Books & Chapters', icon: Bookmark, count: stats?.books_chapters || 3141 },
    { id: 'patents', label: 'Patents', icon: Lightbulb, count: stats?.patents || 600 },
    { id: 'internships', label: 'Internships & MoUs', icon: Briefcase, count: (stats?.training_internships || 649) + (stats?.mous_collaborations || 437) },
    { id: 'news', label: 'News & Events', icon: Calendar, count: stats?.news_events || 30 },
    { id: 'directory', label: 'Web Directory', icon: Globe, count: (stats?.page_index || 199) + (stats?.data_tables_catalogue || 94) },
    { id: 'placements_scholarships', label: 'Placements & Scholarships', icon: Award, count: '400+ / 100%' },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4 bg-slate-900/60 backdrop-blur-md">
      <div className="bg-[#e0e5ec] border border-white/90 rounded-[28px] sm:rounded-[36px] w-full max-w-6xl max-h-[94vh] flex flex-col shadow-neu-extruded-lg overflow-hidden text-slate-800">
        
        {/* Modal Top Header */}
        <div className="flex items-center justify-between px-4 py-3.5 sm:px-6 sm:py-4 border-b border-white/60 bg-[#e0e5ec] shadow-neu-extruded-sm shrink-0">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center shadow-neu-blue-glow border border-white/40">
              <Database className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h2 className="text-base sm:text-lg font-black text-slate-900 tracking-tight">
                  Kalinga University Database & Knowledge Portal
                </h2>
                <span className="hidden md:inline-block px-2.5 py-0.5 rounded-full text-[10px] font-black bg-blue-100 text-blue-800 border border-blue-200 shadow-sm">
                  {stats?.total_records ? `${stats.total_records.toLocaleString()} Grounded Records` : '11,000+ Grounded Records'}
                </span>
              </div>
              <p className="text-[11px] text-slate-500 font-semibold">
                Official SQLite Database with full-text search across all published university datasets
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-9 h-9 rounded-2xl text-slate-600 hover:text-slate-900 bg-[#e0e5ec] shadow-neu-button active:shadow-neu-button-active flex items-center justify-center transition-all border border-white/70 shrink-0"
            title="Close modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Scrollable Tab Navigation Bar */}
        <div className="flex border-b border-white/60 px-3 sm:px-6 bg-[#e0e5ec] overflow-x-auto scrollbar-none gap-2 py-2.5 shrink-0">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => {
                  setActiveTab(tab.id as TabType);
                  loadTabData(tab.id as TabType);
                }}
                className={`flex items-center space-x-1.5 py-2 px-3 rounded-2xl text-xs font-black whitespace-nowrap transition-all border ${
                  isActive
                    ? 'bg-gradient-to-br from-[#f0f5fc] to-[#d2d7de] text-blue-800 shadow-neu-pressed border-blue-300'
                    : 'text-slate-600 hover:text-slate-900 bg-gradient-to-br from-[#f0f5fc] to-[#d2d7de] shadow-neu-button active:shadow-neu-button-active border-white/80'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-blue-600' : 'text-slate-500'}`} />
                <span>{tab.label}</span>
                <span className={`ml-1 text-[10px] px-1.5 py-0.2 rounded-full font-bold ${isActive ? 'bg-blue-600 text-white' : 'bg-slate-200/80 text-slate-600'}`}>
                  {tab.count}
                </span>
              </button>
            );
          })}
        </div>

        {/* Tab Content Body */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 text-slate-700 bg-[#e0e5ec]">
          {loading ? (
            <div className="flex flex-col items-center justify-center py-20 text-slate-600">
              <div className="w-8 h-8 border-3 border-blue-600 border-t-transparent rounded-full animate-spin mb-3"></div>
              <p className="text-xs font-bold">Querying official university database...</p>
            </div>
          ) : (
            <div>

              {/* 1. GLOBAL FTS SEARCH TAB */}
              {activeTab === 'search' && (
                <div className="space-y-4">
                  <form onSubmit={handleGlobalSearch} className="flex flex-col sm:flex-row gap-2">
                    <div className="relative flex-1">
                      <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                      <input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        placeholder="Search anything: 'Computer Science', 'Ideathon', 'Dr. Biradar', 'Scopus', 'B.Tech', 'Scholarship'..."
                        className="w-full pl-10 pr-4 py-2.5 text-xs sm:text-sm rounded-2xl bg-[#e0e5ec] border border-white/90 shadow-neu-pressed focus:outline-none focus:ring-2 focus:ring-blue-500 font-semibold"
                      />
                    </div>
                    <select
                      value={searchFilter}
                      onChange={(e) => setSearchFilter(e.target.value)}
                      className="px-3 py-2 text-xs rounded-2xl bg-[#e0e5ec] border border-white/80 shadow-neu-button text-slate-700 font-bold focus:outline-none"
                    >
                      <option value="">All Categories</option>
                      <option value="course">Courses</option>
                      <option value="faq">Course FAQs</option>
                      <option value="career_path">Career Paths</option>
                      <option value="research_paper">Research Papers</option>
                      <option value="book_chapter">Books & Chapters</option>
                      <option value="patent">Patents</option>
                      <option value="news_event">News & Events</option>
                      <option value="internship">Internships</option>
                      <option value="mou">MoUs</option>
                      <option value="page">Web Pages</option>
                    </select>
                    <button
                      type="submit"
                      className="px-5 py-2.5 rounded-2xl bg-gradient-to-r from-blue-600 to-indigo-700 text-white text-xs font-black shadow-neu-blue-glow hover:opacity-95 transition-all"
                    >
                      Search Database
                    </button>
                  </form>

                  {searchResults.length > 0 ? (
                    <div className="space-y-3">
                      <div className="text-xs font-bold text-slate-500">
                        Found {searchResults.length} matching records across database:
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {searchResults.map((r, idx) => (
                          <div key={idx} className="bg-[#e0e5ec] border border-white/90 rounded-2xl p-4 shadow-neu-extruded-sm flex flex-col justify-between">
                            <div>
                              <div className="flex items-center justify-between mb-1.5">
                                <span className="text-[10px] font-black uppercase px-2 py-0.5 rounded-md bg-blue-100 text-blue-800 border border-blue-200">
                                  {r.entity_type?.replace('_', ' ')}
                                </span>
                                {r.source_url && (
                                  <a
                                    href={r.source_url}
                                    target="_blank"
                                    rel="noreferrer"
                                    className="text-blue-600 hover:text-blue-800 text-[11px] font-bold flex items-center space-x-1"
                                  >
                                    <span>Source</span>
                                    <ExternalLink className="w-3 h-3" />
                                  </a>
                                )}
                              </div>
                              <h4 className="text-xs font-black text-slate-900 leading-snug">{r.title}</h4>
                              {r.subtitle && <p className="text-[11px] text-blue-700 font-bold mt-0.5">{r.subtitle}</p>}
                              <p className="text-xs text-slate-600 font-medium mt-2 line-clamp-3">{r.content}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  ) : searchQuery ? (
                    <div className="text-center py-10 text-xs text-slate-500 font-bold">
                      No matching records found for "{searchQuery}". Try broader keywords like "Engineering", "Management", "Science", "Patent".
                    </div>
                  ) : (
                    <div className="bg-[#e0e5ec] border border-white/90 rounded-2xl p-6 shadow-neu-extruded text-center space-y-2">
                      <Search className="w-8 h-8 text-blue-600 mx-auto" />
                      <h3 className="text-sm font-black text-slate-800">Unified University Full-Text Search (FTS5)</h3>
                      <p className="text-xs text-slate-500 max-w-lg mx-auto">
                        Search across 10,967 indexed items including 4,869 research papers, 3,141 book chapters, 600 patents, 649 internships, 438 MoUs, 355 FAQs, 621 career paths, and 69 courses.
                      </p>
                    </div>
                  )}
                </div>
              )}

              {/* 2. PROGRAMS & FEES TAB */}
              {activeTab === 'fees' && (
                <div className="space-y-4">
                  {/* Filter and Search Controls */}
                  <div className="flex flex-col sm:flex-row items-center justify-between gap-2.5">
                    <div className="flex items-center space-x-1.5 w-full sm:w-auto overflow-x-auto pb-1 sm:pb-0">
                      {['ALL', 'UG', 'PG', 'Diploma'].map((lvl) => (
                        <button
                          key={lvl}
                          onClick={() => setFeesLevelFilter(lvl)}
                          className={`px-3 py-1.5 rounded-xl text-xs font-bold border transition-all whitespace-nowrap ${
                            feesLevelFilter === lvl
                              ? 'bg-blue-600 text-white shadow-neu-blue-glow border-blue-500'
                              : 'bg-[#e0e5ec] text-slate-700 border-white/80 shadow-neu-button active:shadow-neu-button-active hover:text-blue-700'
                          }`}
                        >
                          {lvl}
                        </button>
                      ))}
                    </div>
                    <div className="flex items-center space-x-2 w-full sm:w-auto">
                      <div className="relative flex-1 sm:w-64">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400" />
                        <input
                          type="text"
                          value={feesSearch}
                          onChange={(e) => setFeesSearch(e.target.value)}
                          placeholder="Search program, degree, or department..."
                          className="w-full pl-9 pr-3 py-1.5 text-xs rounded-xl bg-[#e0e5ec] border border-white/80 shadow-neu-pressed focus:outline-none font-semibold"
                        />
                      </div>
                      <button
                        onClick={() => loadTabData('fees')}
                        title="Reload from Live Database"
                        className="p-2 rounded-xl text-slate-600 hover:text-blue-700 bg-[#e0e5ec] border border-white/80 shadow-neu-button active:shadow-neu-button-active transition-all shrink-0"
                      >
                        <RefreshCw className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>

                  {/* Summary Bar */}
                  <div className="flex items-center justify-between text-[11px] font-bold text-slate-500 px-1">
                    <span>
                      Showing <strong className="text-blue-800">{filteredFees.length}</strong> of {feesData.length} Programs & Fees Schedules
                      {feesLevelFilter !== 'ALL' && <span className="ml-1 text-slate-600">(Level: {feesLevelFilter})</span>}
                      {feesSearch && <span className="ml-1 text-slate-600">(Query: "{feesSearch}")</span>}
                    </span>
                    {(feesLevelFilter !== 'ALL' || feesSearch) && (
                      <button
                        onClick={() => {
                          setFeesLevelFilter('ALL');
                          setFeesSearch('');
                        }}
                        className="text-blue-600 hover:text-blue-800 text-[11px] font-extrabold underline"
                      >
                        Reset Filters
                      </button>
                    )}
                  </div>

                  {/* Table or Empty State */}
                  {filteredFees.length > 0 ? (
                    <div className="overflow-x-auto rounded-3xl border border-white/80 shadow-neu-pressed p-1.5 bg-[#e0e5ec]">
                      <table className="w-full text-left text-xs border-collapse">
                        <thead>
                          <tr className="bg-[#e0e5ec] text-slate-800 border-b border-slate-300 font-extrabold">
                            <th className="p-3">Program & Department</th>
                            <th className="p-3">Duration</th>
                            <th className="p-3">Tuition / Sem</th>
                            <th className="p-3">Exam Fee / Sem</th>
                            <th className="p-3">Total Published Fee</th>
                            <th className="p-3">Official Link</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-300/60">
                          {filteredFees.map((r: any, idx: number) => {
                            const tuitionDisplay = r.tuition_fee_per_sem || (r.tuition_per_semester_inr ? `₹${r.tuition_per_semester_inr}` : 'Contact University');
                            const examFeeDisplay = r.exam_fee_per_sem || (r.exam_fee_per_semester_inr ? `₹${r.exam_fee_per_semester_inr}/sem` : '₹1,500/sem');
                            const totalDisplay = r.published_total || (r.total_fees_inr ? `₹${r.total_fees_inr}` : 'Contact University');
                            const durationDisplay = r.duration || (r.tenure_years ? `${r.tenure_years} Years` : '—');
                            const sourceUrl = r.official_source || r.url || 'https://kalingauniversity.ac.in/ku-fees';

                            return (
                              <tr key={idx} className="hover:bg-blue-50/60 transition-colors">
                                <td className="p-3">
                                  <div className="font-bold text-slate-900">{r.program}</div>
                                  <div className="flex items-center space-x-1.5 mt-0.5">
                                    {r.short_name && <span className="text-[10px] text-blue-700 font-semibold">{r.short_name}</span>}
                                    {r.level && (
                                      <span className="text-[9px] font-bold px-1.5 py-0.2 rounded bg-slate-200 text-slate-700">
                                        {r.level}
                                      </span>
                                    )}
                                    {r.department && (
                                      <span className="text-[10px] text-slate-500 font-medium hidden sm:inline">
                                        • {r.department}
                                      </span>
                                    )}
                                  </div>
                                </td>
                                <td className="p-3 text-slate-600 font-medium whitespace-nowrap">{durationDisplay}</td>
                                <td className="p-3 text-emerald-700 font-extrabold whitespace-nowrap">{tuitionDisplay}</td>
                                <td className="p-3 text-slate-600 font-medium whitespace-nowrap">{examFeeDisplay}</td>
                                <td className="p-3 text-blue-700 font-black whitespace-nowrap">{totalDisplay}</td>
                                <td className="p-3">
                                  {sourceUrl && (
                                    <a
                                      href={sourceUrl}
                                      target="_blank"
                                      rel="noreferrer"
                                      className="inline-flex items-center space-x-1 text-blue-600 hover:text-blue-800 font-bold text-[11px]"
                                    >
                                      <span>Portal</span>
                                      <ExternalLink className="w-3 h-3" />
                                    </a>
                                  )}
                                </td>
                              </tr>
                            );
                          })}
                        </tbody>
                      </table>
                    </div>
                  ) : (
                    <div className="bg-[#e0e5ec] border border-white/90 rounded-2xl p-8 text-center shadow-neu-extruded space-y-3">
                      <p className="text-sm font-black text-slate-700">
                        No programs found matching {feesSearch ? `"${feesSearch}"` : ''} under level filter "{feesLevelFilter}".
                      </p>
                      <p className="text-xs text-slate-500 max-w-md mx-auto">
                        Try clearing your search query or selecting "ALL" to browse all 69 programs and fee structures.
                      </p>
                      <button
                        onClick={() => {
                          setFeesLevelFilter('ALL');
                          setFeesSearch('');
                        }}
                        className="px-4 py-2 rounded-xl text-xs font-bold text-white bg-blue-600 shadow-neu-blue-glow hover:bg-blue-700 transition-all"
                      >
                        Reset All Filters
                      </button>
                    </div>
                  )}
                </div>
              )}

              {/* 3. COURSE FAQS TAB */}
              {activeTab === 'faqs' && (
                <div className="space-y-4">
                  <div className="relative">
                    <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <input
                      type="text"
                      value={faqsSearch}
                      onChange={(e) => setFaqsSearch(e.target.value)}
                      placeholder="Search 355 course FAQs: e.g. 'eligibility', 'animation', 'syllabus', 'career'..."
                      className="w-full pl-10 pr-4 py-2.5 text-xs sm:text-sm rounded-2xl bg-[#e0e5ec] border border-white/90 shadow-neu-pressed focus:outline-none font-semibold"
                    />
                  </div>
                  <div className="text-xs font-bold text-slate-500">
                    Showing {filteredFaqs.length} FAQs
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                    {filteredFaqs.slice(0, 40).map((f: any, idx: number) => (
                      <div key={idx} className="bg-[#e0e5ec] border border-white/90 rounded-2xl p-4 shadow-neu-extruded-sm">
                        <span className="text-[10px] font-black uppercase text-blue-700 bg-blue-50 px-2 py-0.5 rounded-md border border-blue-200">
                          {f.course}
                        </span>
                        <h4 className="text-xs font-extrabold text-slate-900 mt-1.5 mb-1">{f.question}</h4>
                        <p className="text-xs text-slate-600 leading-relaxed">{f.answer}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 4. CAREER PATHS TAB */}
              {activeTab === 'career_paths' && (
                <div className="space-y-4">
                  <div className="relative">
                    <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <input
                      type="text"
                      value={careerSearch}
                      onChange={(e) => setCareerSearch(e.target.value)}
                      placeholder="Search 621 career pathways: e.g. 'Software Engineer', 'Data Analyst', 'Cybersecurity'..."
                      className="w-full pl-10 pr-4 py-2.5 text-xs sm:text-sm rounded-2xl bg-[#e0e5ec] border border-white/90 shadow-neu-pressed focus:outline-none font-semibold"
                    />
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                    {filteredCareers.slice(0, 45).map((c: any, idx: number) => (
                      <div key={idx} className="bg-[#e0e5ec] border border-white/90 rounded-2xl p-4 shadow-neu-extruded-sm flex flex-col justify-between">
                        <div>
                          <span className="text-[10px] font-black text-blue-700 uppercase bg-blue-50 px-2 py-0.5 rounded-md">
                            {c.course}
                          </span>
                          <h4 className="text-xs font-black text-slate-900 mt-2">{c.career_path}</h4>
                          <p className="text-[11px] text-slate-600 mt-1 font-medium leading-relaxed">{c.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 5. RESEARCH PAPERS TAB */}
              {activeTab === 'research' && (
                <div className="space-y-4">
                  <form onSubmit={handlePapersSearchSubmit} className="flex gap-2">
                    <div className="relative flex-1">
                      <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                      <input
                        type="text"
                        value={papersSearch}
                        onChange={(e) => setPapersSearch(e.target.value)}
                        placeholder="Search 4,869 Scopus & UGC Care papers by title, author, journal..."
                        className="w-full pl-10 pr-4 py-2.5 text-xs rounded-2xl bg-[#e0e5ec] border border-white/90 shadow-neu-pressed focus:outline-none font-semibold"
                      />
                    </div>
                    <button
                      type="submit"
                      className="px-4 py-2 rounded-2xl bg-blue-600 text-white text-xs font-black shadow-neu-blue-glow"
                    >
                      Search
                    </button>
                  </form>

                  <div className="flex items-center justify-between text-xs font-bold text-slate-500">
                    <span>
                      Total Published Papers: {papersData?.total?.toLocaleString() || '4,866'} | Page {papersPage} of {papersData?.total_pages || 244}
                    </span>
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => changePapersPage(papersPage - 1)}
                        disabled={papersPage <= 1}
                        className="p-1.5 rounded-xl bg-[#e0e5ec] border border-white/80 shadow-neu-button disabled:opacity-40"
                      >
                        <ChevronLeft className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => changePapersPage(papersPage + 1)}
                        disabled={papersData && papersPage >= papersData.total_pages}
                        className="p-1.5 rounded-xl bg-[#e0e5ec] border border-white/80 shadow-neu-button disabled:opacity-40"
                      >
                        <ChevronRight className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  <div className="space-y-3">
                    {papersData?.papers?.map((p: any, idx: number) => (
                      <div key={idx} className="bg-[#e0e5ec] border border-white/90 rounded-2xl p-4 shadow-neu-extruded-sm">
                        <div className="flex items-start justify-between gap-2">
                          <h4 className="text-xs font-black text-slate-900 leading-snug">{p.title}</h4>
                          <span className="text-[10px] font-black px-2 py-0.5 rounded-md bg-emerald-100 text-emerald-800 shrink-0">
                            {p.year}
                          </span>
                        </div>
                        <div className="text-[11px] text-blue-800 font-bold mt-1">
                          Author: {p.authors} ({p.department})
                        </div>
                        <div className="text-[11px] text-slate-600 font-medium mt-0.5">
                          Journal: <span className="font-semibold">{p.journal}</span> • ISSN: {p.issn} • {p.indexing}
                        </div>
                        {p.url && (
                          <div className="mt-2">
                            <a
                              href={p.url}
                              target="_blank"
                              rel="noreferrer"
                              className="text-blue-600 hover:text-blue-800 text-[11px] font-bold inline-flex items-center space-x-1"
                            >
                              <span>View Publication / Scopus Record</span>
                              <ExternalLink className="w-3 h-3" />
                            </a>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 6. BOOKS & CHAPTERS TAB */}
              {activeTab === 'books' && (
                <div className="space-y-4">
                  <form onSubmit={handleBooksSearchSubmit} className="flex gap-2">
                    <div className="relative flex-1">
                      <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                      <input
                        type="text"
                        value={booksSearch}
                        onChange={(e) => setBooksSearch(e.target.value)}
                        placeholder="Search 3,141 books & chapters by title, teacher name, publisher..."
                        className="w-full pl-10 pr-4 py-2.5 text-xs rounded-2xl bg-[#e0e5ec] border border-white/90 shadow-neu-pressed focus:outline-none font-semibold"
                      />
                    </div>
                    <button
                      type="submit"
                      className="px-4 py-2 rounded-2xl bg-blue-600 text-white text-xs font-black shadow-neu-blue-glow"
                    >
                      Search
                    </button>
                  </form>

                  <div className="flex items-center justify-between text-xs font-bold text-slate-500">
                    <span>
                      Total Publications: {booksData?.total?.toLocaleString() || '3,141'} | Page {booksPage} of {booksData?.total_pages || 158}
                    </span>
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => changeBooksPage(booksPage - 1)}
                        disabled={booksPage <= 1}
                        className="p-1.5 rounded-xl bg-[#e0e5ec] border border-white/80 shadow-neu-button disabled:opacity-40"
                      >
                        <ChevronLeft className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => changeBooksPage(booksPage + 1)}
                        disabled={booksData && booksPage >= booksData.total_pages}
                        className="p-1.5 rounded-xl bg-[#e0e5ec] border border-white/80 shadow-neu-button disabled:opacity-40"
                      >
                        <ChevronRight className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  <div className="space-y-3">
                    {booksData?.books?.map((b: any, idx: number) => (
                      <div key={idx} className="bg-[#e0e5ec] border border-white/90 rounded-2xl p-4 shadow-neu-extruded-sm">
                        <div className="flex items-start justify-between gap-2">
                          <h4 className="text-xs font-black text-slate-900 leading-snug">{b.title}</h4>
                          <span className="text-[10px] font-black px-2 py-0.5 rounded-md bg-indigo-100 text-indigo-800 shrink-0">
                            {b.year}
                          </span>
                        </div>
                        <div className="text-[11px] text-blue-800 font-bold mt-1">
                          Teacher: {b.author} ({b.department})
                        </div>
                        <div className="text-[11px] text-slate-600 font-medium mt-0.5">
                          Publisher: <span className="font-semibold">{b.publisher || 'Kalinga University'}</span> • ISBN/ISSN: {b.isbn || 'N/A'} • {b.nat_intl}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 7. PATENTS TAB */}
              {activeTab === 'patents' && (
                <div className="space-y-4">
                  <div className="relative">
                    <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <input
                      type="text"
                      value={patentsSearch}
                      onChange={(e) => setPatentsSearch(e.target.value)}
                      placeholder="Search 600 patents: e.g. 'Dr. Praveen', 'Spectroscopy', 'Solar', 'Grant'..."
                      className="w-full pl-10 pr-4 py-2.5 text-xs sm:text-sm rounded-2xl bg-[#e0e5ec] border border-white/90 shadow-neu-pressed focus:outline-none font-semibold"
                    />
                  </div>
                  <div className="text-xs font-bold text-slate-500">
                    Showing {filteredPatents.length} Patents
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                    {filteredPatents.slice(0, 40).map((p: any, idx: number) => (
                      <div key={idx} className="bg-[#e0e5ec] border border-white/90 rounded-2xl p-4 shadow-neu-extruded-sm flex flex-col justify-between">
                        <div>
                          <div className="flex items-center justify-between mb-1.5">
                            <span className="text-[10px] font-black px-2 py-0.5 rounded-md bg-emerald-100 text-emerald-800 border border-emerald-200">
                              {p.status || 'Published'}
                            </span>
                            <span className="text-[10px] text-slate-500 font-bold">{p.date}</span>
                          </div>
                          <h4 className="text-xs font-black text-slate-900 leading-snug">{p.topic}</h4>
                          <p className="text-[11px] text-blue-700 font-bold mt-1">Inventor: {p.inventor} ({p.faculty})</p>
                          <p className="text-[11px] text-slate-500 font-semibold mt-0.5">Application No: {p.app_no}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 8. INTERNSHIPS & MOUS TAB */}
              {activeTab === 'internships' && (
                <div className="space-y-4">
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => setInternshipsSubTab('internships')}
                      className={`px-3 py-1.5 rounded-xl text-xs font-bold border transition-all ${
                        internshipsSubTab === 'internships'
                          ? 'bg-blue-600 text-white shadow-neu-blue-glow border-blue-500'
                          : 'bg-[#e0e5ec] text-slate-700 border-white/80 shadow-neu-button'
                      }`}
                    >
                      Training & Internships (649)
                    </button>
                    <button
                      onClick={() => setInternshipsSubTab('mous')}
                      className={`px-3 py-1.5 rounded-xl text-xs font-bold border transition-all ${
                        internshipsSubTab === 'mous'
                          ? 'bg-blue-600 text-white shadow-neu-blue-glow border-blue-500'
                          : 'bg-[#e0e5ec] text-slate-700 border-white/80 shadow-neu-button'
                      }`}
                    >
                      MoUs & Collaborations (438)
                    </button>
                  </div>

                  <div className="relative">
                    <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <input
                      type="text"
                      value={internshipsSearch}
                      onChange={(e) => setInternshipsSearch(e.target.value)}
                      placeholder={internshipsSubTab === 'internships' ? "Search student or company (e.g. LG, Apollo, TCS)..." : "Search MoU partner or faculty..."}
                      className="w-full pl-10 pr-4 py-2 text-xs rounded-2xl bg-[#e0e5ec] border border-white/90 shadow-neu-pressed focus:outline-none font-semibold"
                    />
                  </div>

                  {internshipsSubTab === 'internships' ? (
                    <div className="overflow-x-auto rounded-3xl border border-white/80 shadow-neu-pressed p-1.5 bg-[#e0e5ec]">
                      <table className="w-full text-left text-xs border-collapse">
                        <thead>
                          <tr className="bg-[#e0e5ec] text-slate-800 border-b border-slate-300 font-extrabold">
                            <th className="p-3">Student Name</th>
                            <th className="p-3">Course / Program</th>
                            <th className="p-3">Company / Industry</th>
                            <th className="p-3">Session</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-300/60">
                          {filteredInternships.slice(0, 50).map((i: any, idx: number) => (
                            <tr key={idx} className="hover:bg-blue-50/60 transition-colors">
                              <td className="p-3 font-bold text-slate-900">{i.student}</td>
                              <td className="p-3 text-slate-600 font-medium">{i.course}</td>
                              <td className="p-3 text-blue-700 font-black">{i.company}</td>
                              <td className="p-3 text-slate-500 text-[11px] font-semibold">{i.session}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  ) : (
                    <div className="overflow-x-auto rounded-3xl border border-white/80 shadow-neu-pressed p-1.5 bg-[#e0e5ec]">
                      <table className="w-full text-left text-xs border-collapse">
                        <thead>
                          <tr className="bg-[#e0e5ec] text-slate-800 border-b border-slate-300 font-extrabold">
                            <th className="p-3">Organisation Partner</th>
                            <th className="p-3">Faculty / Discipline</th>
                            <th className="p-3">Duration</th>
                            <th className="p-3">Category</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-300/60">
                          {filteredMous.slice(0, 50).map((m: any, idx: number) => (
                            <tr key={idx} className="hover:bg-blue-50/60 transition-colors">
                              <td className="p-3 font-bold text-slate-900">{m.partner}</td>
                              <td className="p-3 text-blue-700 font-semibold">{m.faculty}</td>
                              <td className="p-3 text-slate-600 text-[11px]">{m.start_date} - {m.end_date}</td>
                              <td className="p-3 text-slate-500 text-[11px]">{m.category}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              )}

              {/* 9. NEWS & EVENTS TAB */}
              {activeTab === 'news' && (
                <div className="space-y-4">
                  <div className="relative">
                    <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <input
                      type="text"
                      value={newsSearch}
                      onChange={(e) => setNewsSearch(e.target.value)}
                      placeholder="Search events, workshops, ideathons..."
                      className="w-full pl-10 pr-4 py-2.5 text-xs sm:text-sm rounded-2xl bg-[#e0e5ec] border border-white/90 shadow-neu-pressed focus:outline-none font-semibold"
                    />
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                    {filteredNews.map((n: any, idx: number) => (
                      <div key={idx} className="bg-[#e0e5ec] border border-white/90 rounded-2xl p-4 shadow-neu-extruded-sm flex flex-col justify-between">
                        <div>
                          <div className="flex items-center justify-between mb-1.5">
                            <span className="text-[10px] font-black px-2 py-0.5 rounded-md bg-amber-100 text-amber-900 border border-amber-200">
                              {n.category || 'Event'}
                            </span>
                            <span className="text-[11px] font-black text-slate-500">{n.date}</span>
                          </div>
                          <h4 className="text-xs font-black text-slate-900 leading-snug">{n.heading}</h4>
                          {n.department && <p className="text-[10px] text-blue-700 font-bold mt-0.5">{n.department}</p>}
                          <p className="text-xs text-slate-600 mt-2 line-clamp-3 leading-relaxed">{n.summary}</p>
                        </div>
                        {n.url && (
                          <div className="mt-3">
                            <a
                              href={n.url}
                              target="_blank"
                              rel="noreferrer"
                              className="text-blue-600 hover:text-blue-800 text-[11px] font-bold inline-flex items-center space-x-1"
                            >
                              <span>Official Event Page</span>
                              <ExternalLink className="w-3 h-3" />
                            </a>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 10. WEB DIRECTORY & CATALOGUE TAB */}
              {activeTab === 'directory' && (
                <div className="space-y-4">
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => setDirectorySubTab('pages')}
                      className={`px-3 py-1.5 rounded-xl text-xs font-bold border transition-all ${
                        directorySubTab === 'pages'
                          ? 'bg-blue-600 text-white shadow-neu-blue-glow border-blue-500'
                          : 'bg-[#e0e5ec] text-slate-700 border-white/80 shadow-neu-button'
                      }`}
                    >
                      Web Pages Index (199)
                    </button>
                    <button
                      onClick={() => setDirectorySubTab('tables')}
                      className={`px-3 py-1.5 rounded-xl text-xs font-bold border transition-all ${
                        directorySubTab === 'tables'
                          ? 'bg-blue-600 text-white shadow-neu-blue-glow border-blue-500'
                          : 'bg-[#e0e5ec] text-slate-700 border-white/80 shadow-neu-button'
                      }`}
                    >
                      Published Data Tables (94)
                    </button>
                  </div>

                  <div className="relative">
                    <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <input
                      type="text"
                      value={directorySearch}
                      onChange={(e) => setDirectorySearch(e.target.value)}
                      placeholder={directorySubTab === 'pages' ? "Search 199 site pages (e.g. NCC, Library, Anti-ragging)..." : "Search 94 data tables..."}
                      className="w-full pl-10 pr-4 py-2 text-xs rounded-2xl bg-[#e0e5ec] border border-white/90 shadow-neu-pressed focus:outline-none font-semibold"
                    />
                  </div>

                  {directorySubTab === 'pages' ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {filteredPages.slice(0, 40).map((p: any, idx: number) => (
                        <div key={idx} className="bg-[#e0e5ec] border border-white/90 rounded-2xl p-3.5 shadow-neu-extruded-sm flex flex-col justify-between">
                          <div>
                            <span className="text-[10px] font-black uppercase text-blue-700 bg-blue-50 px-2 py-0.5 rounded-md">
                              /{p.slug}
                            </span>
                            <h4 className="text-xs font-black text-slate-900 mt-1">{p.title}</h4>
                            <p className="text-[11px] text-slate-500 mt-1 line-clamp-2">{p.meta_description}</p>
                          </div>
                          <div className="mt-2.5">
                            <a
                              href={p.url}
                              target="_blank"
                              rel="noreferrer"
                              className="text-blue-600 hover:text-blue-800 text-[11px] font-bold inline-flex items-center space-x-1"
                            >
                              <span>Visit Page</span>
                              <ExternalLink className="w-3 h-3" />
                            </a>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {filteredTables.map((t: any, idx: number) => (
                        <div key={idx} className="bg-[#e0e5ec] border border-white/90 rounded-2xl p-3.5 shadow-neu-extruded-sm">
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-[10px] font-black text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded-md">
                              {t.category || 'University Table'}
                            </span>
                            <span className="text-[10px] text-slate-500 font-bold">{t.rows} rows • {t.columns} cols</span>
                          </div>
                          <h4 className="text-xs font-black text-slate-900">{t.title}</h4>
                          <p className="text-[10px] text-slate-500 font-mono mt-1 line-clamp-2">{t.headers}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* 11. PLACEMENTS & SCHOLARSHIPS TAB */}
              {activeTab === 'placements_scholarships' && (
                <div className="space-y-5">
                  {/* Scholarships Card */}
                  {scholarshipsData?.data && (
                    <div className="space-y-3">
                      <div className="bg-[#e0e5ec] border border-white/90 rounded-2xl p-4 shadow-neu-extruded flex items-center justify-between">
                        <div>
                          <h3 className="text-sm font-extrabold text-slate-900">Scholarships Up To 100%</h3>
                          <p className="text-xs text-blue-700 font-bold mt-0.5">{scholarshipsData.data.total_distributed_claim}</p>
                        </div>
                        <Award className="w-8 h-8 text-amber-500 drop-shadow-sm" />
                      </div>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        {scholarshipsData.data.categories?.map((cat: any, idx: number) => (
                          <div key={idx} className="bg-[#e0e5ec] border border-white/90 rounded-2xl p-3.5 shadow-neu-extruded-sm">
                            <div className="text-xs font-extrabold text-blue-700 mb-1">{cat.category}</div>
                            <div className="text-xs text-slate-600 font-medium">{cat.details}</div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Placements Cards */}
                  {placementsData?.data && (
                    <div className="space-y-3 pt-2">
                      <h3 className="text-xs font-extrabold text-slate-800 uppercase tracking-wider">Published Student Placement Highlights</h3>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        {placementsData.data.published_individual_examples?.map((ex: any, idx: number) => (
                          <div key={idx} className="bg-[#e0e5ec] border border-white/90 rounded-2xl p-3.5 shadow-neu-extruded flex items-center justify-between">
                            <div>
                              <div className="text-xs font-bold text-slate-900">{ex.student} ({ex.program})</div>
                              <div className="text-xs text-slate-500 font-semibold">{ex.company}</div>
                            </div>
                            <div className="text-xs font-black text-emerald-700 bg-[#e0e5ec] px-3 py-1 rounded-xl border border-white/80 shadow-neu-pressed">
                              {ex.package}
                            </div>
                          </div>
                        ))}
                      </div>

                      <div className="pt-2">
                        <h4 className="text-xs font-extrabold text-slate-800 mb-2">Recruitment Partners (400+ Claimed)</h4>
                        <div className="flex flex-wrap gap-2">
                          {placementsData.data.recruiters?.map((rec: string, idx: number) => (
                            <span key={idx} className="px-3 py-1 rounded-xl bg-gradient-to-br from-[#f0f5fc] to-[#d2d7de] text-xs font-bold text-slate-800 border border-white/80 shadow-neu-button">
                              {rec}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}

            </div>
          )}
        </div>

      </div>
    </div>
  );
};
