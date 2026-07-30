// Ativer Projetos e Soluções - Application Logic
// Core Tech Stack: Three.js, GSAP, Lenis Smooth Scroll

document.addEventListener("DOMContentLoaded", () => {
  // 1. Preloader Dismissal
  const preloader = document.getElementById("preloader");
  window.addEventListener("load", () => {
    gsap.to(preloader, {
      opacity: 0,
      duration: 1,
      ease: "power2.out",
      onComplete: () => {
        preloader.style.display = "none";
        // Trigger initial Hero animations
        triggerHeroAnimations();
      }
    });
  });

  // Fallback for preloader in case load event takes too long
  setTimeout(() => {
    if (preloader.style.display !== "none") {
      gsap.to(preloader, {
        opacity: 0,
        duration: 0.8,
        ease: "power2.out",
        onComplete: () => {
          preloader.style.display = "none";
          triggerHeroAnimations();
        }
      });
    }
  }, 3000);

  // Set current year in footer
  document.getElementById("year").textContent = new Date().getFullYear();

  // 2. Custom Interactive Cursor
  const cursor = document.getElementById("custom-cursor");
  const cursorFollower = document.getElementById("custom-cursor-follower");
  let mouseX = 0, mouseY = 0;
  let followerX = 0, followerY = 0;

  document.addEventListener("mousemove", (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;

    // Direct cursor positioning
    gsap.set(cursor, { x: mouseX, y: mouseY });
  });

  // Follower interpolation for premium buttery delay
  gsap.ticker.add(() => {
    followerX += (mouseX - followerX) * 0.15;
    followerY += (mouseY - followerY) * 0.15;
    gsap.set(cursorFollower, { x: followerX, y: followerY });
  });

  // Cursor Hover listeners for links and interactive targets
  const hoverTargets = document.querySelectorAll("[data-cursor-hover], a, button, select, input, textarea, .project-card");
  hoverTargets.forEach((target) => {
    target.addEventListener("mouseenter", () => {
      document.body.classList.add("hovering-link");
    });
    target.addEventListener("mouseleave", () => {
      document.body.classList.remove("hovering-link");
    });
  });

  // 3. Lenis Smooth Scroll Initialization
  const lenis = new Lenis({
    duration: 1.2,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    orientation: 'vertical',
    gestureOrientation: 'vertical',
    smoothWheel: true,
    wheelMultiplier: 1,
    touchMultiplier: 2,
    infinite: false,
  });

  function raf(time) {
    lenis.raf(time);
    requestAnimationFrame(raf);
  }
  requestAnimationFrame(raf);

  // Synchronize ScrollTrigger with Lenis
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((time) => {
    lenis.raf(time * 1000);
  });
  gsap.ticker.lagSmoothing(0);

  // Smooth scroll to anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        lenis.scrollTo(targetElement);
        // If mobile menu is open, close it
        if (isMobileMenuOpen) {
          toggleMobileMenu();
        }
      }
    });
  });

  // 4. Interactive Three.js Particle Background (Hero Section)
  initThreeBackground();

  // 5. GSAP Scroll Animations
  initScrollAnimations();

  // 6. Portfolio Case Filtration
  initPortfolioFilters();

  // 7. Interactive Numbers Counter
  initCounterAnimations();

  // 8. Testimonials Auto-Slider
  initTestimonialsSlider();

  // 9. Interactive Timeline Active Progress Line
  initTimelineProgress();
});

// Hero animations trigger on page load
function triggerHeroAnimations() {
  const tl = gsap.timeline();
  tl.from(".reveal-text", {
    y: 50,
    opacity: 0,
    duration: 1.2,
    ease: "power4.out"
  })
  .from("#hero p", {
    y: 30,
    opacity: 0,
    duration: 0.8,
    ease: "power3.out"
  }, "-=0.8")
  .from("#hero .flex", {
    y: 20,
    opacity: 0,
    duration: 0.6,
    ease: "power2.out"
  }, "-=0.5")
  .from("header", {
    y: -30,
    opacity: 0,
    duration: 0.8,
    ease: "power2.out"
  }, "-=0.6");
}

// Three.js interactive glowing particle constellation network
function initThreeBackground() {
  const container = document.getElementById("three-canvas-container");
  if (!container) return;

  // Scene setup
  const scene = new THREE.Scene();

  // Camera setup
  const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
  camera.position.z = 100;

  // Renderer setup
  const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.appendChild(renderer.domElement);

  // Create Constellation Points
  const particlesCount = window.innerWidth < 768 ? 100 : 250;
  const geometry = new THREE.BufferGeometry();
  const positions = new Float32Array(particlesCount * 3);
  const speeds = [];

  for (let i = 0; i < particlesCount * 3; i += 3) {
    // Distribute points in space
    positions[i] = (Math.random() - 0.5) * 200;     // X
    positions[i + 1] = (Math.random() - 0.5) * 200; // Y
    positions[i + 2] = (Math.random() - 0.5) * 200; // Z

    speeds.push({
      x: (Math.random() - 0.5) * 0.1,
      y: (Math.random() - 0.5) * 0.1,
      z: (Math.random() - 0.5) * 0.1
    });
  }

  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

  // Particle texture material using Canvas-generated round particle
  const pCanvas = document.createElement('canvas');
  pCanvas.width = 16;
  pCanvas.height = 16;
  const ctx = pCanvas.getContext('2d');
  const gradient = ctx.createRadialGradient(8, 8, 0, 8, 8, 8);
  gradient.addColorStop(0, 'rgba(0, 212, 255, 1)');
  gradient.addColorStop(0.3, 'rgba(0, 102, 255, 0.8)');
  gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, 16, 16);

  const pTexture = new THREE.CanvasTexture(pCanvas);

  const material = new THREE.PointsMaterial({
    size: 2.5,
    map: pTexture,
    transparent: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
  });

  const particleSystem = new THREE.Points(geometry, material);
  scene.add(particleSystem);

  // Line connections between near particles
  const lineMaterial = new THREE.LineBasicMaterial({
    color: 0x0066ff,
    transparent: true,
    opacity: 0.08,
    blending: THREE.AdditiveBlending
  });

  let lineGeometry = new THREE.BufferGeometry();
  let linePositions = new Float32Array(particlesCount * particlesCount * 6);
  lineGeometry.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
  let lineMesh = new THREE.LineSegments(lineGeometry, lineMaterial);
  scene.add(lineMesh);

  // Mouse interactivity variables
  let targetMouseX = 0, targetMouseY = 0;
  let curMouseX = 0, curMouseY = 0;

  window.addEventListener('mousemove', (e) => {
    targetMouseX = (e.clientX - window.innerWidth / 2) * 0.1;
    targetMouseY = (e.clientY - window.innerHeight / 2) * 0.1;
  });

  // Animation loop
  function animate() {
    requestAnimationFrame(animate);

    // Smoothly interpolate camera position towards mouse offset
    curMouseX += (targetMouseX - curMouseX) * 0.05;
    curMouseY += (targetMouseY - curMouseY) * 0.05;

    camera.position.x = curMouseX;
    camera.position.y = -curMouseY;
    camera.lookAt(scene.position);

    const positionsArr = particleSystem.geometry.attributes.position.array;

    // Update particle coordinates
    let index = 0;
    let lineIndex = 0;
    const maxConnectionDist = 35;

    for (let i = 0; i < particlesCount; i++) {
      const idx = i * 3;

      // Add speed offset
      positionsArr[idx] += speeds[i].x;
      positionsArr[idx + 1] += speeds[i].y;
      positionsArr[idx + 2] += speeds[i].z;

      // Boundary collision checks (bounce back)
      if (Math.abs(positionsArr[idx]) > 100) speeds[i].x *= -1;
      if (Math.abs(positionsArr[idx + 1]) > 100) speeds[i].y *= -1;
      if (Math.abs(positionsArr[idx + 2]) > 100) speeds[i].z *= -1;
    }

    // Dynamic Line Generation (for particles within max distance threshold)
    for (let i = 0; i < particlesCount; i++) {
      for (let j = i + 1; j < particlesCount; j++) {
        const dx = positionsArr[i * 3] - positionsArr[j * 3];
        const dy = positionsArr[i * 3 + 1] - positionsArr[j * 3 + 1];
        const dz = positionsArr[i * 3 + 2] - positionsArr[j * 3 + 2];
        const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);

        if (dist < maxConnectionDist) {
          linePositions[lineIndex++] = positionsArr[i * 3];
          linePositions[lineIndex++] = positionsArr[i * 3 + 1];
          linePositions[lineIndex++] = positionsArr[i * 3 + 2];

          linePositions[lineIndex++] = positionsArr[j * 3];
          linePositions[lineIndex++] = positionsArr[j * 3 + 1];
          linePositions[lineIndex++] = positionsArr[j * 3 + 2];
        }
      }
    }

    particleSystem.geometry.attributes.position.needsUpdate = true;
    lineGeometry.setAttribute('position', new THREE.BufferAttribute(linePositions.slice(0, lineIndex), 3));
    lineGeometry.attributes.position.needsUpdate = true;

    // Slow overall rotation for aesthetic floatiness
    particleSystem.rotation.y += 0.001;
    lineMesh.rotation.y += 0.001;

    renderer.render(scene, camera);
  }

  animate();

  // Resize handler
  window.addEventListener('resize', () => {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
  });
}

// GSAP elegant scroll animations
function initScrollAnimations() {
  gsap.registerPlugin(ScrollTrigger);

  // Elegant fade-in up on service cards
  gsap.from("#services .glass-panel", {
    scrollTrigger: {
      trigger: "#services",
      start: "top 80%",
    },
    y: 50,
    opacity: 0,
    duration: 0.8,
    stagger: 0.15,
    ease: "power2.out"
  });

  // Fade and scale for the visual block in About Section
  gsap.from("#about .glass-panel", {
    scrollTrigger: {
      trigger: "#about",
      start: "top 75%",
    },
    scale: 0.95,
    opacity: 0,
    duration: 1.2,
    ease: "power3.out"
  });

  // Parallax elements scroll effects
  gsap.from("#sustainability .glass-panel", {
    scrollTrigger: {
      trigger: "#sustainability",
      start: "top 85%",
    },
    x: 40,
    opacity: 0,
    duration: 1,
    ease: "power2.out"
  });
}

// Portfolio/Cases categories filtering
function initPortfolioFilters() {
  const filters = document.querySelectorAll(".project-filter");
  const items = document.querySelectorAll(".project-item");

  filters.forEach(filter => {
    filter.addEventListener("click", () => {
      // Toggle active classes on filters
      filters.forEach(f => f.classList.remove("active", "border-brandSecondary", "bg-brandSecondary/10", "text-white"));
      filters.forEach(f => f.classList.add("border-white/10", "text-brandTextMuted"));

      filter.classList.add("active", "border-brandSecondary", "bg-brandSecondary/10", "text-white");
      filter.classList.remove("border-white/10", "text-brandTextMuted");

      const category = filter.getAttribute("data-filter");

      // Animate grid change
      items.forEach(item => {
        if (category === "all" || item.getAttribute("data-category") === category) {
          item.style.display = "flex";
          gsap.fromTo(item, { scale: 0.9, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "power2.out" });
        } else {
          gsap.to(item, {
            scale: 0.9,
            opacity: 0,
            duration: 0.2,
            onComplete: () => {
              item.style.display = "none";
            }
          });
        }
      });
    });
  });
}

// Dynamic Counter Numbers Incrementation via GSAP Trigger
function initCounterAnimations() {
  const counters = document.querySelectorAll(".count");
  counters.forEach(counter => {
    const target = parseInt(counter.getAttribute("data-target"));

    ScrollTrigger.create({
      trigger: counter,
      start: "top 90%",
      onEnter: () => {
        let obj = { value: 0 };
        gsap.to(obj, {
          value: target,
          duration: 2,
          ease: "power3.out",
          onUpdate: () => {
            counter.textContent = Math.floor(obj.value);
          }
        });
      },
      once: true
    });
  });
}

// Testimonials auto sliding mechanism
function initTestimonialsSlider() {
  const slider = document.getElementById("testimonial-slider-container");
  const slides = slider.children;
  const prevBtn = document.getElementById("slider-prev");
  const nextBtn = document.getElementById("slider-next");
  let currentIndex = 0;
  const slideCount = slides.length;

  function updateSliderPosition() {
    gsap.to(slider, {
      x: `-${currentIndex * 100}%`,
      duration: 0.6,
      ease: "power3.out"
    });
  }

  nextBtn.addEventListener("click", () => {
    currentIndex = (currentIndex + 1) % slideCount;
    updateSliderPosition();
  });

  prevBtn.addEventListener("click", () => {
    currentIndex = (currentIndex - 1 + slideCount) % slideCount;
    updateSliderPosition();
  });

  // Optional: Auto sliding every 6 seconds
  setInterval(() => {
    currentIndex = (currentIndex + 1) % slideCount;
    updateSliderPosition();
  }, 6000);
}

// Timeline animated active pipeline
function initTimelineProgress() {
  const timelineProgress = document.getElementById("timeline-progress-line");
  if (!timelineProgress) return;

  ScrollTrigger.create({
    trigger: "#process",
    start: "top 40%",
    end: "bottom 60%",
    onUpdate: (self) => {
      // Map self.progress directly to the timeline line width
      gsap.to(timelineProgress, { width: `${self.progress * 100}%`, duration: 0.1 });
    }
  });
}

// Lead Form / Budget Modal Handlers
const budgetModal = document.getElementById("budget-modal");

function openModal() {
  budgetModal.classList.remove("pointer-events-none");
  gsap.to(budgetModal, { opacity: 1, duration: 0.3, ease: "power2.out" });
}

function closeModal() {
  gsap.to(budgetModal, {
    opacity: 0,
    duration: 0.3,
    ease: "power2.in",
    onComplete: () => {
      budgetModal.classList.add("pointer-events-none");
      // Reset success window
      document.getElementById("form-success").classList.add("opacity-0", "pointer-events-none");
    }
  });
}

function handleFormSubmit(event) {
  event.preventDefault();
  // Simulate API Lead validation and collection
  const name = document.getElementById("name").value;
  const company = document.getElementById("company").value;
  const phone = document.getElementById("phone").value;
  const email = document.getElementById("email").value;
  const message = document.getElementById("message").value;

  console.log("Ativer Lead Captured:", { name, company, phone, email, message });

  // Display success animation window
  const successDiv = document.getElementById("form-success");
  successDiv.classList.remove("pointer-events-none");
  gsap.to(successDiv, { opacity: 1, duration: 0.4 });

  // Reset form fields
  document.getElementById("contact-form").reset();
}

// Mobile Menu Navigation Handlers
let isMobileMenuOpen = false;
const mobileMenuBtn = document.getElementById("mobile-menu-btn");
const mobileMenu = document.getElementById("mobile-menu");
const bar1 = document.getElementById("bar1");
const bar2 = document.getElementById("bar2");
const bar3 = document.getElementById("bar3");

mobileMenuBtn.addEventListener("click", toggleMobileMenu);

function toggleMobileMenu() {
  isMobileMenuOpen = !isMobileMenuOpen;
  if (isMobileMenuOpen) {
    mobileMenu.classList.remove("translate-x-full");
    bar1.style.transform = "rotate(45deg) translate(5px, 5px)";
    bar2.style.opacity = "0";
    bar3.style.transform = "rotate(-45deg) translate(5px, -5px)";
  } else {
    mobileMenu.classList.add("translate-x-full");
    bar1.style.transform = "none";
    bar2.style.opacity = "1";
    bar3.style.transform = "none";
  }
}

// Floating Header solid glass shadow styling on scroll
window.addEventListener("scroll", () => {
  const header = document.querySelector("header");
  if (window.scrollY > 50) {
    header.querySelector("div").classList.add("bg-brandDark/80", "backdrop-blur-md", "shadow-xl", "border-b", "border-white/5", "rounded-full", "mt-2", "py-2");
  } else {
    header.querySelector("div").classList.remove("bg-brandDark/80", "backdrop-blur-md", "shadow-xl", "border-b", "border-white/5", "rounded-full", "mt-2", "py-2");
  }
});

// Case Projects Details Storage
const projectsData = {
  retro_clp: {
    title: "Retrofit de CLP e Sistema Supervisório SCADA",
    category: "Automação Industrial",
    desc: "A Ativer Projetos liderou o processo completo de retrofit tecnológico para uma grande metalúrgica de autopeças. O CLP legado foi substituído por uma arquitetura redundante baseada no processador Siemens S7-1500, integrada a remotas descentralizadas ET200SP via rede Profinet.<br><br>O sistema supervisório de última geração oferece relatórios analíticos automáticos de picos térmicos, contagem de peças e alertas preditivos de manutenção, permitindo à equipe de coordenação mitigar paradas não programadas.",
    techs: "Siemens TIA Portal, Ignition SCADA, Profinet, Modbus TCP",
    roi: "+24% em OEE, -45% tempo de parada",
    img: "assets/images/img_3.png"
  },
  eta_auto: {
    title: "Automação de ETA Industrial de Alta Vazão",
    category: "ETA & ETE",
    desc: "Desenvolvimento de engenharia de automação, instrumentação e controle fino para Estação de Tratamento de Água (ETA) industrial de 120m³/h de capacidade.<br><br>Foi implementado um algoritmo avançado de controle proporcional integral derivativo (PID) para a dosagem otimizada de coagulante e cloro ativo em função da turbidez instantânea medida no campo. As telas de supervisão dão controle total sobre as bombas elevatórias, filtros rápidos de areia e carvão ativo, gerando enorme economia de químicos.",
    techs: "Rockwell CompactLogix, FactoryTalk View, Sensores Endress+Hauser",
    roi: "-30% em consumo químico, 100% de reuso",
    img: "assets/images/img_5.png"
  },
  ccm_auto: {
    title: "Painéis TTA / PTTA Certificados",
    category: "Projetos e Painéis",
    desc: "Projeto e fabricação interna sob medida de painéis elétricos inteligentes do tipo Centro de Controle de Motores (CCM) extraíveis para acionamento de sopradores e bombas de lavagem de alta vazão.<br><br>Montado e testado sob rigorosos critérios da norma técnica NBR IEC 61439-1, o painel é equipado com relés de proteção avançados e relés térmicos eletrônicos inteligentes que transmitem informações analíticas de corrente elétrica e temperatura de cada motor.",
    techs: "EPLAN Pro Panel, Disjuntores Schneider, Barramentos Estanhados",
    roi: "Segurança total NR-10, Fácil manutenção rápida",
    img: "assets/images/img_0.png"
  },
  scada_sist: {
    title: "Supervisão de Utilidades em Tempo Real",
    category: "Automação Industrial",
    desc: "Integração completa de rede de utilidades industriais englobando geração de vapor, compressores de ar e sistemas de resfriamento (chillers) com aquisição unificada em servidor local.<br><br>Com telas intuitivas e responsivas de alta legibilidade que exibem mapas térmicos, relatórios inteligentes de conformidade e detecção automática de falhas estruturais, a Ativer simplificou e refinou toda a gestão de manufatura do parceiro.",
    techs: "GE iFIX, Protocolo OPC UA, Medidores Multikron",
    roi: "-18% desperdício de energia, Start-up imediato",
    img: "assets/images/img_2.png"
  },
  ete_quim: {
    title: "Automação de ETE de Indústria de Bebidas",
    category: "ETA & ETE",
    desc: "Projeto de engenharia de automação integral para sistema de tratamento biológico aeróbio por lodos ativados de efluente orgânico agroindustrial.<br><br>Desenvolvemos malhas de controle inteligentes que modulam a rotação dos sopradores centrífugos de oxigênio em tempo real, baseando-se no valor exato de oxigênio dissolvido coletado pelas sondas de imersão. Garantia de enquadramento absoluto aos rigorosos padrões de descarte ecológico.",
    techs: "Schneider M340, Vijeo Citect, Transmissores de Oxigênio Dissolvido",
    roi: "-32% consumo energético de sopradores",
    img: "assets/images/img_1.png"
  },
  proj_eplan: {
    title: "Projetos Elétricos e Modelagem 3D",
    category: "Projetos e Painéis",
    desc: "Elaboração de projetos executivos de sistemas elétricos industriais complexos para subestações, plantas de força e sistemas de controle.<br><br>O projeto, inteiramente modelado e documentado utilizando a plataforma profissional EPLAN, garante precisão milimétrica de barramentos, layout interno otimizado tridimensional dos painéis e geração imediata de listas de materiais exatas de montagem, otimizando de forma robusta o CAPEX do cliente.",
    techs: "EPLAN Electric P8, EPLAN Cabinet, Dimensionamento de Proteção",
    roi: "-25% tempo de fabricação, Documentação AS-BUILT",
    img: "assets/images/img_4.png"
  }
};

const projectModal = document.getElementById("project-modal");

function openProjectModal(projectId) {
  const data = projectsData[projectId];
  if (!data) return;

  document.getElementById("modal-project-img").src = data.img;
  document.getElementById("modal-project-category").textContent = `// ${data.category.toUpperCase()}`;
  document.getElementById("modal-project-title").textContent = data.title;
  document.getElementById("modal-project-desc").innerHTML = data.desc;
  document.getElementById("modal-project-techs").textContent = data.techs;
  document.getElementById("modal-project-roi").textContent = data.roi;

  projectModal.classList.remove("pointer-events-none");
  gsap.to(projectModal, { opacity: 1, duration: 0.3, ease: "power2.out" });
}

function closeProjectModal() {
  gsap.to(projectModal, {
    opacity: 0,
    duration: 0.3,
    ease: "power2.in",
    onComplete: () => {
      projectModal.classList.add("pointer-events-none");
    }
  });
}
