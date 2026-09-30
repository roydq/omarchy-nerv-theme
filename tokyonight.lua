-- NERV palette for tokyonight.nvim: warning orange on black, emergency red,
-- MAGI green and Unit-01 purple, tuned for reading code (the generic mapping
-- from colors.toml is too orange). Omarchy doesn't load it; it's for a
-- tokyonight setup that registers it as a style, see the README.
---@type Palette
return {
  accent = '#ff6a00', -- float and picker borders
  bg = '#060504',
  bg_dark = '#030202',
  bg_dark1 = '#000000',
  bg_highlight = '#1a0f07',
  blue = '#ffb347', -- functions
  blue0 = '#7a3000', -- search, selection
  blue1 = '#b48cff', -- types
  blue2 = '#2fe6e6', -- info
  blue5 = '#ff8c42', -- operators
  blue6 = '#ffe2c2',
  blue7 = '#4d2a0f', -- diff change
  comment = '#8a6a50',
  cyan = '#ff8c42', -- keywords (non-treesitter)
  dark3 = '#5c4030',
  dark5 = '#8f6e55',
  fg = '#f4e6d4',
  fg_dark = '#d9c2a8',
  fg_gutter = '#3d2a1c',
  green = '#6dff9a', -- strings
  green1 = '#ffcc99', -- properties
  green2 = '#3dff7a',
  magenta = '#ff7a1a',
  magenta2 = '#ff1f5a',
  orange = '#ffcc00', -- constants, numbers
  purple = '#ff6a00', -- keywords
  red = '#ff4d4d',
  red1 = '#ff2a2a', -- errors
  teal = '#2fe6e6',
  terminal_black = '#3d2a1c',
  yellow = '#ffbb7a', -- parameters
  git = {
    add = '#3dff7a',
    change = '#ffb347',
    delete = '#ff2a2a',
  },
}
