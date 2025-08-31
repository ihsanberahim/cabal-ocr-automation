# Multi-Offensive Stats Implementation Guide

## Overview
This document outlines the step-by-step implementation of adding support for 3 offensive stats with priority-based fallback logic to the Arrival Skill automation system.

## Problem Statement
The original system only supported 1 offensive stat and 1 defensive stat. Users wanted the ability to specify multiple offensive stats with fallback logic - if the 1st priority offensive stat doesn't match, automatically try the 2nd, then 3rd.

## Implementation Steps

### Step 1: UI Modifications (arrival_tab.py)

#### 1.1 Replace Single Offensive Stat Section
**File:** `unified_game_automation/ui/arrival_tab.py`
**Lines:** 82-95

**Before:**
```python
# Offensive stat selection
off_frame = ttk.Frame(stats_frame)
off_frame.pack(fill=tk.X, pady=2)

ttk.Label(off_frame, text="Offensive Stat:").pack(side=tk.LEFT)
self.off_stat = tk.StringVar()

offensive_skills = [""] + get_offensive_skills()  # Add empty option
self.off_stat_dropdown = ttk.Combobox(off_frame, textvariable=self.off_stat, values=offensive_skills, state="readonly", width=20)
self.off_stat_dropdown.pack(side=tk.LEFT, padx=(5, 0))
self.off_stat_dropdown.bind("<<ComboboxSelected>>", self.update_off_variations)

ttk.Label(off_frame, text="Min Value:").pack(side=tk.LEFT, padx=(10, 0))
self.off_var = tk.StringVar()
self.off_var_dropdown = ttk.Combobox(off_frame, textvariable=self.off_var, state="readonly", width=8)
self.off_var_dropdown.pack(side=tk.LEFT, padx=(5, 0))
```

**After:**
```python
# Offensive stat selection - 1st priority
off_frame1 = ttk.Frame(stats_frame)
off_frame1.pack(fill=tk.X, pady=2)

ttk.Label(off_frame1, text="Offensive Stat (1st):").pack(side=tk.LEFT)
self.off_stat1 = tk.StringVar()

offensive_skills = [""] + get_offensive_skills()  # Add empty option
self.off_stat1_dropdown = ttk.Combobox(off_frame1, textvariable=self.off_stat1, values=offensive_skills, state="readonly", width=20)
self.off_stat1_dropdown.pack(side=tk.LEFT, padx=(5, 0))
self.off_stat1_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_off_variations(1))

ttk.Label(off_frame1, text="Min Value:").pack(side=tk.LEFT, padx=(10, 0))
self.off_var1 = tk.StringVar()
self.off_var1_dropdown = ttk.Combobox(off_frame1, textvariable=self.off_var1, state="readonly", width=8)
self.off_var1_dropdown.pack(side=tk.LEFT, padx=(5, 0))

# Offensive stat selection - 2nd priority
off_frame2 = ttk.Frame(stats_frame)
off_frame2.pack(fill=tk.X, pady=2)

ttk.Label(off_frame2, text="Offensive Stat (2nd):").pack(side=tk.LEFT)
self.off_stat2 = tk.StringVar()

self.off_stat2_dropdown = ttk.Combobox(off_frame2, textvariable=self.off_stat2, values=offensive_skills, state="readonly", width=20)
self.off_stat2_dropdown.pack(side=tk.LEFT, padx=(5, 0))
self.off_stat2_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_off_variations(2))

ttk.Label(off_frame2, text="Min Value:").pack(side=tk.LEFT, padx=(10, 0))
self.off_var2 = tk.StringVar()
self.off_var2_dropdown = ttk.Combobox(off_frame2, textvariable=self.off_var2, state="readonly", width=8)
self.off_var2_dropdown.pack(side=tk.LEFT, padx=(5, 0))

# Offensive stat selection - 3rd priority
off_frame3 = ttk.Frame(stats_frame)
off_frame3.pack(fill=tk.X, pady=2)

ttk.Label(off_frame3, text="Offensive Stat (3rd):").pack(side=tk.LEFT)
self.off_stat3 = tk.StringVar()

self.off_stat3_dropdown = ttk.Combobox(off_frame3, textvariable=self.off_stat3, values=offensive_skills, state="readonly", width=20)
self.off_stat3_dropdown.pack(side=tk.LEFT, padx=(5, 0))
self.off_stat3_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_off_variations(3))

ttk.Label(off_frame3, text="Min Value:").pack(side=tk.LEFT, padx=(10, 0))
self.off_var3 = tk.StringVar()
self.off_var3_dropdown = ttk.Combobox(off_frame3, textvariable=self.off_var3, state="readonly", width=8)
self.off_var3_dropdown.pack(side=tk.LEFT, padx=(5, 0))
```

#### 1.2 Update Helper Method
**File:** `unified_game_automation/ui/arrival_tab.py`
**Lines:** 230-245

**Before:**
```python
def update_off_variations(self, event=None):
    """Update the offensive stat variations dropdown based on selected stat"""
    selected_stat = self.off_stat.get()
    if selected_stat:
        variations = get_stat_variations(selected_stat)
        self.off_var_dropdown['values'] = variations
        if variations:
            self.off_var.set(variations[0])  # Select first variation by default
    else:
        self.off_var_dropdown['values'] = []
        self.off_var.set("")
```

**After:**
```python
def update_off_variations(self, stat_number, event=None):
    """Update the offensive stat variations dropdown based on selected stat"""
    if stat_number == 1:
        selected_stat = self.off_stat1.get()
        dropdown = self.off_var1_dropdown
        var = self.off_var1
    elif stat_number == 2:
        selected_stat = self.off_stat2.get()
        dropdown = self.off_var2_dropdown
        var = self.off_var2
    elif stat_number == 3:
        selected_stat = self.off_stat3.get()
        dropdown = self.off_var3_dropdown
        var = self.off_var3
    else:
        return

    if selected_stat:
        variations = get_stat_variations(selected_stat)
        dropdown['values'] = variations
        if variations:
            var.set(variations[0])  # Select first variation by default
    else:
        dropdown['values'] = []
        var.set("")
```

#### 1.3 Update Start Automation Method
**File:** `unified_game_automation/ui/arrival_tab.py`
**Lines:** 270-310

**Before:**
```python
def start_automation(self):
    """Start the arrival skill automation"""
    # Check if another tool is running
    if not self.main_window.set_running_tool("Arrival Skill"):
        return

    # Check if at least one stat is specified
    if not self.off_stat.get() and not self.def_stat.get():
        messagebox.showerror("Error", "Please specify at least one stat to look for.")
        self.main_window.clear_running_tool()
        return

    # Prepare desired stats
    desired_stats = {
        'offensive': [],
        'defensive': []
    }

    # Add offensive stat if specified
    stat_name = self.off_stat.get()
    if stat_name:
        variation = self.off_var.get()
        if not variation:
            messagebox.showerror("Error", f"Please select a minimum value for {stat_name}.")
            self.main_window.clear_running_tool()
            return

        # Extract numeric value from the variation
        value_match = re.search(r'(\d+)', variation)
        if value_match:
            off_val = int(value_match.group(1))
            desired_stats['offensive'].append((stat_name, off_val, variation))
            self.main_window.update_status(f"Looking for {stat_name} with minimum value {variation}")

    # Add defensive stat if specified
    stat_name = self.def_stat.get()
    if stat_name:
        variation = self.def_var.get()
        if not variation:
            messagebox.showerror("Error", f"Please select a minimum value for {stat_name}.")
            self.main_window.clear_running_tool()
            return

        # Extract numeric value from the variation
        value_match = re.search(r'(\d+)', variation)
        if value_match:
            def_val = int(value_match.group(1))
            desired_stats['defensive'].append((stat_name, def_val, variation))
            self.main_window.update_status(f"Looking for {stat_name} with minimum value {variation}")

    # Start automation
    if self.automation.start(desired_stats):
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.main_window.update_status("Arrival skill automation started")
    else:
        self.main_window.clear_running_tool()
```

**After:**
```python
def start_automation(self):
    """Start the arrival skill automation"""
    # Check if another tool is running
    if not self.main_window.set_running_tool("Arrival Skill"):
        return

    # Check if at least one stat is specified
    if not (self.off_stat1.get() or self.off_stat2.get() or self.off_stat3.get() or self.def_stat.get()):
        messagebox.showerror("Error", "Please specify at least one stat to look for.")
        self.main_window.clear_running_tool()
        return

    # Prepare desired stats
    desired_stats = {
        'offensive': [],
        'defensive': []
    }

    # Add offensive stats if specified (in priority order)
    for stat_num in [1, 2, 3]:
        if stat_num == 1:
            stat_name = self.off_stat1.get()
            variation = self.off_var1.get()
        elif stat_num == 2:
            stat_name = self.off_stat2.get()
            variation = self.off_var2.get()
        elif stat_num == 3:
            stat_name = self.off_stat3.get()
            variation = self.off_var3.get()

        if stat_name:
            if not variation:
                messagebox.showerror("Error", f"Please select a minimum value for {stat_name}.")
                self.main_window.clear_running_tool()
                return

            # Extract numeric value from the variation
            value_match = re.search(r'(\d+)', variation)
            if value_match:
                off_val = int(value_match.group(1))
                desired_stats['offensive'].append((stat_name, off_val, variation))
                self.main_window.update_status(f"Looking for {stat_name} with minimum value {variation}")

    # Add defensive stat if specified
    stat_name = self.def_stat.get()
    if stat_name:
        variation = self.def_var.get()
        if not variation:
            messagebox.showerror("Error", f"Please select a minimum value for {stat_name}.")
            self.main_window.clear_running_tool()
            return

        # Extract numeric value from the variation
        value_match = re.search(r'(\d+)', variation)
        if value_match:
            def_val = int(value_match.group(1))
            desired_stats['defensive'].append((stat_name, def_val, variation))
            self.main_window.update_status(f"Looking for {stat_name} with minimum value {variation}")

    # Start automation
    if self.automation.start(desired_stats):
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.main_window.update_status("Arrival skill automation started")
    else:
        self.main_window.clear_running_tool()
```

### Step 2: Automation Logic Modifications (arrival_automation.py)

#### 2.1 Update Check Desired Stats Method
**File:** `unified_game_automation/automation/arrival_automation.py`
**Lines:** 280-320

**Before:**
```python
def check_desired_stats(self, current_stats, desired_stats):
    """
    Check if current stats meet the desired criteria for arrival skills
    - If only offensive stat specified: The offensive stat must be found
    - If only defensive stat specified: The defensive stat must be found
    - If both are specified: Both the offensive AND defensive stat must be found
    """
    if not desired_stats:
        return True

    if not desired_stats.get('offensive') and not desired_stats.get('defensive'):
        return True

    # Check if offensive stat matches (if specified)
    off_match = False
    if desired_stats.get('offensive'):
        display_stat_name, min_value, _ = desired_stats['offensive'][0]
        base_stat_name = get_base_stat_name(display_stat_name)

        if base_stat_name in current_stats:
            stat_value = current_stats[base_stat_name]
            if stat_value is None:
                # Special case: arrival skill detected but value unavailable due to UI collision
                self.update_status(f"🎉 FOUND: {display_stat_name} detected!")
                self.update_status(f"⚠️ Note: Cannot verify value due to UI collision - please check manually")
                self.stop()
                messagebox.showinfo("Found it!", f"{display_stat_name} detected!\n\nNote: Cannot read value due to UI collision.\nPlease verify the value manually.")
                return True
            elif stat_value >= min_value:
                off_match = True
                self.update_status(f"✅ MATCH: Found {display_stat_name} with value {stat_value} (target: {min_value}+)")
    else:
        off_match = True

    # Check if defensive stat matches (if specified)
    def_match = False
    if desired_stats.get('defensive'):
        display_stat_name, min_value, _ = desired_stats['defensive'][0]
        base_stat_name = get_base_stat_name(display_stat_name)

        if base_stat_name in current_stats:
            stat_value = current_stats[base_stat_name]
            if stat_value is None:
                # Special case: arrival skill detected but value unavailable due to UI collision
                self.update_status(f"🎉 FOUND: {display_stat_name} detected!")
                self.update_status(f"⚠️ Note: Cannot verify value due to UI collision - please check manually")
                self.stop()
                messagebox.showinfo("Found it!", f"{display_stat_name} detected!\n\nNote: Cannot read value due to UI collision.\nPlease verify the value manually.")
                return True
            elif stat_value >= min_value:
                def_match = True
                self.update_status(f"✅ MATCH: Found {display_stat_name} with value {stat_value} (target: {min_value}+)")
    else:
        def_match = True

    return off_match and def_match
```

**After:**
```python
def check_desired_stats(self, current_stats, desired_stats):
    """
    Check if current stats meet the desired criteria for arrival skills
    - If multiple offensive stats specified: Check them in order (1st, 2nd, 3rd) - any match is success
    - If only defensive stat specified: The defensive stat must be found
    - If both are specified: Any offensive stat AND the defensive stat must be found
    """
    if not desired_stats:
        return True

    if not desired_stats.get('offensive') and not desired_stats.get('defensive'):
        return True

    # Check if any offensive stat matches (if specified) - try in priority order
    off_match = False
    if desired_stats.get('offensive'):
        for i, (display_stat_name, min_value, variation) in enumerate(desired_stats['offensive'], 1):
            base_stat_name = get_base_stat_name(display_stat_name)

            if base_stat_name in current_stats:
                stat_value = current_stats[base_stat_name]
                if stat_value is None:
                    # Special case: arrival skill detected but value unavailable due to UI collision
                    self.update_status(f"🎉 FOUND: {display_stat_name} detected! (Priority {i})")
                    self.update_status(f"⚠️ Note: Cannot verify value due to UI collision - please check manually")
                    self.stop()
                    messagebox.showinfo("Found it!", f"{display_stat_name} detected!\n\nNote: Cannot read value due to UI collision.\nPlease verify the value manually.")
                    return True
                elif stat_value >= min_value:
                    off_match = True
                    self.update_status(f"✅ MATCH: Found {display_stat_name} with value {stat_value} (target: {min_value}+) - Priority {i}")
                    break  # Found a match, no need to check lower priority stats
                else:
                    self.update_status(f"❌ {display_stat_name} found but value {stat_value} < {min_value} - trying next priority")
            else:
                self.update_status(f"❌ {display_stat_name} not found - trying next priority")
    else:
        off_match = True

    # Check if defensive stat matches (if specified)
    def_match = False
    if desired_stats.get('defensive'):
        display_stat_name, min_value, _ = desired_stats['defensive'][0]
        base_stat_name = get_base_stat_name(display_stat_name)

        if base_stat_name in current_stats:
            stat_value = current_stats[base_stat_name]
            if stat_value is None:
                # Special case: arrival skill detected but value unavailable due to UI collision
                self.update_status(f"🎉 FOUND: {display_stat_name} detected!")
                self.update_status(f"⚠️ Note: Cannot verify value due to UI collision - please check manually")
                self.stop()
                messagebox.showinfo("Found it!", f"{display_stat_name} detected!\n\nNote: Cannot read value due to UI collision.\nPlease verify the value manually.")
                return True
            elif stat_value >= min_value:
                def_match = True
                self.update_status(f"✅ MATCH: Found {display_stat_name} with value {stat_value} (target: {min_value}+)")
    else:
        def_match = True

    return off_match and def_match
```

## Testing Steps

### 1. UI Testing
1. Launch the application
2. Navigate to the "Arrival Skill" tab
3. Verify that 3 offensive stat dropdowns are visible:
   - "Offensive Stat (1st):"
   - "Offensive Stat (2nd):"
   - "Offensive Stat (3rd):"
4. Test dropdown functionality:
   - Select different offensive stats in each dropdown
   - Verify that min value dropdowns populate correctly
   - Test that all 3 can be set independently

### 2. Logic Testing
1. Set up test scenario:
   - Set "All Attack Up." as 1st priority with min value "All Attack Up. (1)"
   - Set "Critical DMG." as 2nd priority with min value "Critical DMG."
   - Set "Add. Damage" as 3rd priority with min value "Add. Damage (1)"
   - Set defensive stat if desired
2. Start automation
3. Verify status messages show priority checking:
   - "❌ All Attack Up. not found - trying next priority"
   - "❌ Critical DMG. not found - trying next priority"
   - "✅ MATCH: Found Add. Damage with value X - Priority 3"

### 3. Edge Case Testing
1. **Empty Stats**: Test with no offensive stats selected
2. **Partial Stats**: Test with only 1st and 3rd priority set (2nd empty)
3. **Value Mismatch**: Test when stat is found but value is too low
4. **UI Collision**: Test when stat is detected but value cannot be read

## Expected Behavior

### Priority Order
1. **1st Priority**: Checked first, if match → success
2. **2nd Priority**: Checked if 1st doesn't match, if match → success
3. **3rd Priority**: Checked if 1st and 2nd don't match, if match → success

### Status Messages
- Clear indication of which priority is being checked
- Feedback when stat is not found or value is insufficient
- Success message shows which priority matched

### Fallback Logic
- Automatic progression through priorities
- No manual intervention required
- Stops at first successful match

## Rollback Plan

If issues arise, the system can be rolled back by:

1. **UI Rollback**: Revert arrival_tab.py to single offensive stat implementation
2. **Logic Rollback**: Revert arrival_automation.py to original check_desired_stats method
3. **Data Structure Rollback**: Ensure desired_stats['offensive'] contains only one item

## Files Modified
1. `unified_game_automation/ui/arrival_tab.py`
   - UI layout changes
   - Helper method updates
   - Start automation logic updates

2. `unified_game_automation/automation/arrival_automation.py`
   - Check desired stats logic
   - Priority-based fallback implementation

## Dependencies
- No new dependencies required
- Uses existing data structures and helper functions
- Maintains backward compatibility with defensive stats
