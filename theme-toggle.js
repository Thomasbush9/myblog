// Theme Toggle for Catppuccin
(function() {
  // Define Catppuccin color schemes
  const themes = {
    dark: {
      '--ctp-rosewater': '#f5e0dc',
      '--ctp-flamingo': '#f2cdcd',
      '--ctp-pink': '#f5c2e7',
      '--ctp-mauve': '#cba6f7',
      '--ctp-red': '#f38ba8',
      '--ctp-maroon': '#eba0ac',
      '--ctp-peach': '#fab387',
      '--ctp-yellow': '#f9e2af',
      '--ctp-green': '#a6e3a1',
      '--ctp-teal': '#94e2d5',
      '--ctp-sky': '#89dceb',
      '--ctp-sapphire': '#74c7ec',
      '--ctp-blue': '#89b4fa',
      '--ctp-lavender': '#b4befe',
      '--ctp-text': '#cdd6f4',
      '--ctp-subtext1': '#bac2de',
      '--ctp-subtext0': '#a6adc8',
      '--ctp-overlay2': '#9399b2',
      '--ctp-overlay1': '#7f849c',
      '--ctp-overlay0': '#6c7086',
      '--ctp-surface2': '#585b70',
      '--ctp-surface1': '#45475a',
      '--ctp-surface0': '#313244',
      '--ctp-base': '#1e1e2e',
      '--ctp-mantle': '#181825',
      '--ctp-crust': '#11111b'
    },
    light: {
      '--ctp-rosewater': '#dc8a78',
      '--ctp-flamingo': '#dd7878',
      '--ctp-pink': '#ea76cb',
      '--ctp-mauve': '#8839ef',
      '--ctp-red': '#d20f39',
      '--ctp-maroon': '#e64553',
      '--ctp-peach': '#fe640b',
      '--ctp-yellow': '#df8e1d',
      '--ctp-green': '#40a02b',
      '--ctp-teal': '#179299',
      '--ctp-sky': '#04a5e5',
      '--ctp-sapphire': '#209fb5',
      '--ctp-blue': '#1e66f5',
      '--ctp-lavender': '#7287fd',
      '--ctp-text': '#4c4f69',
      '--ctp-subtext1': '#5c5f77',
      '--ctp-subtext0': '#6c6f85',
      '--ctp-overlay2': '#7c7f93',
      '--ctp-overlay1': '#8c8fa1',
      '--ctp-overlay0': '#9ca0b0',
      '--ctp-surface2': '#acb0be',
      '--ctp-surface1': '#bcc0cc',
      '--ctp-surface0': '#ccd0da',
      '--ctp-base': '#eff1f5',
      '--ctp-mantle': '#e6e9ef',
      '--ctp-crust': '#dce0e8'
    }
  };

  function applyTheme(theme) {
    const root = document.documentElement;
    const colors = themes[theme];
    
    for (const [property, value] of Object.entries(colors)) {
      root.style.setProperty(property, value);
    }
    
    root.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }

  function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
    updateToggleButton(newTheme);
  }

  function updateToggleButton(theme) {
    const button = document.getElementById('theme-toggle');
    if (button) {
      button.textContent = theme === 'dark' ? '☀️' : '🌙';
      button.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`);
    }
  }

  function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    applyTheme(savedTheme);
    
    // Wait for navbar to load then add toggle button
    const checkExist = setInterval(() => {
      const navbar = document.querySelector('.navbar-right');
      if (navbar) {
        clearInterval(checkExist);
        addToggleButton();
      }
    }, 100);
  }

  function addToggleButton() {
    const navbarRight = document.querySelector('.navbar-right');
    if (navbarRight) {
      // Check if button already exists
      if (!document.getElementById('theme-toggle')) {
        const button = document.createElement('button');
        button.id = 'theme-toggle';
        button.className = 'theme-toggle-btn';
        button.onclick = toggleTheme;
        button.setAttribute('aria-label', 'Toggle theme');
        
        navbarRight.insertBefore(button, navbarRight.firstChild);
        
        // Update button with current theme
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
        updateToggleButton(currentTheme);
      }
    }
  }

  // Initialize theme on page load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTheme);
  } else {
    initTheme();
  }

  // Expose toggle function globally for debugging
  window.toggleTheme = toggleTheme;
})();
